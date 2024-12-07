# =====================================================================
from util._models.company import Company
from util._models.continent import Continent
from util._models.country import Country as Model
from util._serializers.country import Country as Serializer
from util._tests.master import MasterTestCase, MasterAPIViewTest

# =====================================================================


class CountryTestCase(MasterTestCase):
    """
    CountryTestCase to handle unit tests for the Country model.
    """

    def setUp(self):
        """
        Set up test data for Country model.
        """
        self.company_ref = Company.objects.create(name="test company")
        self.continent_ref = Continent.objects.create(
            company=self.company_ref, name="test continent"
        )
        self.model_name = "test Country"
        self.model_ref = Model.objects.create(
            company=self.company_ref,
            continent=self.continent_ref,
            name=self.model_name,
            iso="100",
            changedBy="tester",
        )

    def test_01(self):
        """
        Test creating a Country model instance.
        """
        self.assertEqual(self.model_ref.name, self.model_name.upper())
        self.assertTrue(self.model_ref.is_active)

    def test_02(self):
        """
        Test updating a Country model instance.
        """
        self.model_ref.changedBy = "tester2"
        self.model_ref.save()
        self.assertEqual(self.model_ref.changedBy, "TESTER2")

    def test_03(self):
        """
        Test the string representation of Country model.
        """
        self.assertEqual(
            str(self.model_ref),
            "{}->{}.{}{}".format(
                self.model_ref.continent,
                self.company_ref,
                "[X]" if self.model_ref.is_active else "[]",
                self.model_name.upper(),
            ),
        )

    def test_04(self):
        """
        Test soft deleting a Country model instance.
        """
        self.model_ref.delete()
        self.assertFalse(
            Model.objects.filter(
                id=self.model_ref.id, is_active=True
            ).exists()
        )

    def test_05(self):
        """
        Test forced deleting a Country model instance.
        """
        self.model_ref.delete(FORCED=True)
        self.assertFalse(Model.objects.filter(id=self.model_ref.id).exists())


class CountryAPIViewTest(MasterAPIViewTest):
    """
    CountryAPIViewTest to handle API tests for the Country model.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        """
        Set up test data for Country API tests.
        """
        self.company_ref = Company.objects.create(
            name="Test company",
        )
        self.continent_ref = Continent.objects.create(
            company=self.company_ref,
            name="Test continent",
        )
        self.url_name = "util__country"
        self.url = self.import_reverse(self.url_name, kwargs={"id": ""})
        self.model_name = "test Country"
        self.iso = "100"
        self.country_data = {
            "company": self.company_ref,
            "continent": self.continent_ref,
            "name": self.model_name,
            "iso": self.iso,
        }
        self.country = Model.objects.create(**self.country_data)
        self.model_name_2 = "Updated Country"
        self.valid_payload = {
            "company": self.company_ref.id,
            "continent": self.continent_ref.id,
            "name": self.model_name_2,
            "iso": self.iso,
        }
        self.invalid_payload = {
            "name": "",
        }

    def test_01(self):
        """
        Test OPTIONS request for Country API.
        """
        response = self.client.options(self.url)
        self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)

    def test_02(self):
        """
        Test GET request for Country API.
        """
        response = self.client.get(self.url)
        Countries = Model.objects.all()
        serializer = Serializer(Countries, many=True)
        self.assertEqual(response.status_code, self.import_status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_03(self):
        """
        Test POST request for creating a Country.
        """
        response = self.client.post(
            self.url, data=self.valid_payload, format="json"
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_201_CREATED
        )
        self.assertEqual(Model.objects.count(), 2)

    def test_04(self):
        """
        Test POST request with invalid data for creating a Country.
        """
        response = self.client.post(
            self.url, data=self.invalid_payload, format="json"
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_400_BAD_REQUEST
        )

    def test_05(self):
        """
        Test PUT request for updating a Country.
        """
        response = self.client.put(
            self.import_reverse(
                self.url_name, kwargs={"id": self.country.pk}
            ),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_202_ACCEPTED
        )
        self.country.refresh_from_db()
        self.assertEqual(
            self.country.name, self.valid_payload["name"].upper()
        )

    def test_06(self):
        """
        Test DELETE request for deleting a Country.
        """
        response = self.client.delete(
            self.import_reverse(self.url_name, kwargs={"id": self.country.pk})
        )
        self.assertEqual(
            response.status_code, self.import_status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Model.objects.filter(pk=self.country.pk, is_active=True).exists()
        )
