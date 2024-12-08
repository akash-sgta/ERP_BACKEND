# =====================================================================
from util._models.company import Company as Model
from util._serializers.company import Company as Serializer
from util._tests.master import MasterTestCase, MasterAPIViewTest

# =====================================================================


class CompanyTestCase(MasterTestCase):
    """
    CompanyTestCase to handle unit tests for the Company model.
    """

    def setUp(self):
        """
        Set up test data for Company model.
        """
        super(CompanyTestCase, self).setUp()
        self.model_name = "test company"
        self.model_ref = Model.objects.create(
            name=self.model_name,
            changedBy="tester",
        )
        self.model_name_2 = "valid company"

    # def test_create_01(self):
    #     """
    #     Test creating a Company model instance.
    #     """
    #     model_ref = Model.objects.create(
    #         name=self.model_name_2,
    #         changedBy="tester",
    #     )
    #     self.assertEqual(model_ref.name, self.model_name_2.upper())
    #     self.assertTrue(model_ref.is_active)

    # def test_create_02(self):
    #     """
    #     Test the check_save method of Company model.
    #     """
    #     result = self.model_ref.check_save()
    #     self.assertTrue(result[0])

    # def test_read_01(self):
    #     """
    #     Test the string representation of Company model.
    #     """
    #     self.assertEqual(
    #         str(self.model_ref),
    #         "{}{}".format(
    #             "[X]" if self.model_ref.is_active else "[]",
    #             self.model_name.upper(),
    #         ),
    #     )

    # def test_update_01(self):
    #     """
    #     Test updating a Company model instance.
    #     """
    #     self.model_ref.changedBy = "tester2"
    #     self.model_ref.save()
    #     self.assertEqual(self.model_ref.changedBy, "tester2".upper())

    # def test_delete_01(self):
    #     """
    #     Test soft deleting a Company model instance.
    #     """
    #     self.model_ref.delete()
    #     self.assertFalse(
    #         Model.objects.filter(
    #             id=self.model_ref.id, is_active=True
    #         ).exists()
    #     )

    # def test_delete_02(self):
    #     """
    #     Test forced deleting a Company model instance.
    #     """
    #     self.model_ref.delete(FORCED=True)
    #     self.assertFalse(Model.objects.filter(id=self.model_ref.id).exists())


class CompanyAPIViewTest(MasterAPIViewTest):
    """
    CompanyAPIViewTest to handle API tests for the Company model.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        """
        Set up test data for Company API tests.
        """
        super(CompanyAPIViewTest, self).setUp()
        self.url_name = "util__company"
        self.url = self.import_reverse(self.url_name, kwargs={"id": ""})
        self.model_name = "test company"
        self.company_data = {"name": self.model_name}
        self.company = Model.objects.create(**self.company_data)
        self.model_name_2 = "Updated company"
        self.valid_payload = {"name": self.model_name_2}
        self.invalid_payload = {"name": ""}

    # def test_read_01(self):
    #     """
    #     Test OPTIONS request for Company API.
    #     """

    #     print(get_user_model().objects.all())

    #     response = self.client.options(self.url, headers=self.headers)
    #     self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)

    # def test_read_02(self):
    #     """
    #     Test GET request for Company API.
    #     """
    #     response = self.client.get(self.url, headers=self.headers)
    #     companies = Model.objects.all()
    #     serializer = Serializer(companies, many=True)
    #     self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)
    #     self.assertEqual(response.data, serializer.data)

    # def test_create_01(self):
    #     """
    #     Test POST request for creating a Company.
    #     """
    #     response = self.client.post(
    #         self.url,
    #         data=self.valid_payload,
    #         format="json",
    #         headers=self.headers,
    #     )
    #     self.assertEqual(
    #         response.status_code, self.import_status.HTTP_201_CREATED
    #     )
    #     self.assertEqual(Model.objects.count(), 2)

    # def test_create_02(self):
    #     """
    #     Test POST request with invalid data for creating a Company.
    #     """
    #     response = self.client.post(
    #         self.url,
    #         data=self.invalid_payload,
    #         format="json",
    #         headers=self.headers,
    #     )
    #     self.assertEqual(
    #         response.status_code, self.import_status.HTTP_400_BAD_REQUEST
    #     )

    # def test_update_01(self):
    #     """
    #     Test PUT request for updating a Company.
    #     """
    #     response = self.client.put(
    #         self.import_reverse(
    #             self.url_name, kwargs={"id": self.company.pk}
    #         ),
    #         data=self.valid_payload,
    #         format="json",
    #         headers=self.headers,
    #     )
    #     self.assertEqual(
    #         response.status_code, self.import_status.HTTP_202_ACCEPTED
    #     )
    #     self.company.refresh_from_db()
    #     self.assertEqual(
    #         self.company.name, self.valid_payload["name"].upper()
    #     )

    # def test_delete_01(self):
    #     """
    #     Test DELETE request for deleting a Company.
    #     """
    #     response = self.client.delete(
    #         self.import_reverse(
    #             self.url_name, kwargs={"id": self.company.pk}
    #         ),
    #         headers=self.headers,
    #     )
    #     self.assertEqual(
    #         response.status_code, self.import_status.HTTP_204_NO_CONTENT
    #     )
    #     self.assertFalse(
    #         Model.objects.filter(pk=self.company.pk, is_active=True).exists()
    #     )
