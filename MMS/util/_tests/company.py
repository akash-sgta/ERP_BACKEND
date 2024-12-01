# =====================================================================
from util._models.company import Company as Model
from util._serializers.company import Company as Serializer
from util._tests.master import MasterTestCase, MasterAPIViewTest

# =====================================================================


class CompanyTestCase(MasterTestCase):

    def setUp(self):
        self.model_name = "test company"
        self.model_ref = Model.objects.create(
            name=self.model_name,
            changedBy="tester",
        )

    def test_create_model_ref(self):
        self.assertEqual(self.model_ref.name, self.model_name.upper())
        self.assertTrue(self.model_ref.is_active)

    def test_update_model_ref(self):
        self.model_ref.changedBy = "tester2"
        self.model_ref.save()
        self.assertEqual(self.model_ref.changedBy, "tester2".upper())

    def test_check_save(self):
        result = self.model_ref.check_save()
        self.assertTrue(result[0])

    def test_str_representation(self):
        self.assertEqual(
            str(self.model_ref),
            "{}{}".format(
                "[X]" if self.model_ref.is_active else "[]",
                self.model_name.upper(),
            ),
        )

    def test_soft_delete(self):
        self.model_ref.delete()
        self.assertFalse(Model.objects.filter(id=self.model_ref.id, is_active=True).exists())

    def test_forced_delete(self):
        self.model_ref.delete(FORCED=True)
        self.assertFalse(Model.objects.filter(id=self.model_ref.id).exists())


class CompanyAPIViewTest(MasterAPIViewTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.url_name = "util__company"
        self.url = self.import_reverse(self.url_name, kwargs={"id": ""})
        self.model_name = "test company"
        self.company_data = {"name": self.model_name}
        self.company = Model.objects.create(**self.company_data)
        self.model_name_2 = "Updated company"
        self.valid_payload = {"name": self.model_name_2}
        self.invalid_payload = {"name": ""}

    def test_options_company(self):
        response = self.client.options(self.url)
        self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)

    def test_get_company(self):
        response = self.client.get(self.url)
        companies = Model.objects.all()
        serializer = Serializer(companies, many=True)
        self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_company(self):
        response = self.client.post(self.url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, self.import_status.HTTP_201_CREATED)
        self.assertEqual(Model.objects.count(), 2)

    def test_post_invalid_company(self):
        response = self.client.post(self.url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, self.import_status.HTTP_400_BAD_REQUEST)

    def test_put_company(self):
        response = self.client.put(
            self.import_reverse(self.url_name, kwargs={"id": self.company.pk}), data=self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, self.import_status.HTTP_202_ACCEPTED)
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, self.valid_payload["name"].upper())

    def test_delete_company(self):
        response = self.client.delete(self.import_reverse(self.url_name, kwargs={"id": self.company.pk}))
        self.assertEqual(response.status_code, self.import_status.HTTP_204_NO_CONTENT)
        self.assertFalse(Model.objects.filter(pk=self.company.pk, is_active=True).exists())
