# =====================================================================
from util._models.company import Company
from util._models.continent import Continent as Model
from util._serializers.continent import Continent as Serializer
from util._tests.master import MasterTestCase, MasterAPIViewTest

# =====================================================================


class ContinentTestCase(MasterTestCase):
    """
    ContinentTestCase to handle unit tests for the Continent model.
    """

    def setUp(self):
        """
        Set up test data for Continent model.
        """
        self.company_ref = Company.objects.create(name="test company")
        self.model_name = "test continent"
        self.model_ref = Model.objects.create(
            company=self.company_ref,
            name=self.model_name,
            changedBy="tester",
        )

    def test_create_01(self):
        """
        Test creating a Continent model instance.
        """
        self.assertEqual(self.model_ref.name, self.model_name.upper())
        self.assertTrue(self.model_ref.is_active)

    def test_update_01(self):
        """
        Test updating a Continent model instance.
        """
        self.model_ref.changedBy = "tester2"
        self.model_ref.save()
        self.assertEqual(self.model_ref.changedBy, "TESTER2")

    def test_read_01(self):
        """
        Test the string representation of Continent model.
        """
        self.assertEqual(
            str(self.model_ref),
            "{}.{}{}".format(
                self.company_ref,
                "[X]" if self.model_ref.is_active else "[]",
                self.model_name.upper(),
            ),
        )

    def test_delete_01(self):
        """
        Test soft deleting a Continent model instance.
        """
        self.model_ref.delete()
        self.assertFalse(
            Model.objects.filter(
                id=self.model_ref.id, is_active=True
            ).exists()
        )

    def test_delete_02(self):
        """
        Test forced deleting a Continent model instance.
        """
        self.model_ref.delete(FORCED=True)
        self.assertFalse(Model.objects.filter(id=self.model_ref.id).exists())


class ContinentAPIViewTest(MasterAPIViewTest):
    """
    ContinentAPIViewTest to handle API tests for the Continent model.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        """
        Set up test data for Continent API tests.
        """
        self.company_ref = Company.objects.create(
            name="Test company",
        )
        self.url_name = "util__continent"
        self.url = self.import_reverse(self.url_name, kwargs={"id": ""})
        self.model_name = "test continent"
        self.continent_data = {
            "company": self.company_ref,
            "name": self.model_name,
        }
        self.continent = Model.objects.create(**self.continent_data)
        self.model_name_2 = "Updated continent"
        self.valid_payload = {"name": self.model_name_2}
        self.invalid_payload = {"name": ""}

    def test_read_01(self):
        """
        Test OPTIONS request for Continent API.
        """
        response = self.client.options(self.url)
        self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)

    def test_read_02(self):
        """
        Test GET request for Continent API.
        """
        response = self.client.get(self.url)
        continents = Model.objects.all()
        serializer = Serializer(continents, many=True)
        self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_01(self):
        """
        Test POST request for creating a Continent.
        """
        response = self.client.post(
            self.url, data=self.valid_payload, format="json"
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_201_CREATED
        )
        self.assertEqual(Model.objects.count(), 2)

    def test_create_02(self):
        """
        Test POST request with invalid data for creating a Continent.
        """
        response = self.client.post(
            self.url, data=self.invalid_payload, format="json"
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_400_BAD_REQUEST
        )

    def test_update_01(self):
        """
        Test PUT request for updating a Continent.
        """
        response = self.client.put(
            self.import_reverse(
                self.url_name, kwargs={"id": self.continent.pk}
            ),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_202_ACCEPTED
        )
        self.continent.refresh_from_db()
        self.assertEqual(
            self.continent.name, self.valid_payload["name"].upper()
        )

    def test_delete_01(self):
        """
        Test DELETE request for deleting a Continent.
        """
        response = self.client.delete(
            self.import_reverse(
                self.url_name, kwargs={"id": self.continent.pk}
            )
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Model.objects.filter(
                pk=self.continent.pk, is_active=True
            ).exists()
        )
