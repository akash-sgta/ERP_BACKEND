# =====================================================================
from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
import base64
from django.contrib.auth import get_user_model
from datetime import datetime

from profile._models.profile import Profile
from util._models.company import Company

# =====================================================================
User = get_user_model()
C_USER_DATA = {
    "username": "admintest",
    "password": "admintest",
    "name": {
        "first": "First",
        "last": "Last",
    },
    "dob": datetime.now(),
}


class MasterTestCase(TestCase):
    """
    MasterTestCase to provide a base class for unit tests.
    """

    def setUp(self):
        """
        Set up test data for the tests.
        """
        try:
            # Create Admin Company
            admin_company_ref = Company.objects.create(
                name="admin", changedBy=C_USER_DATA["username"]
            )
            # Create user
            user_ref = User.objects.create_user(
                username=C_USER_DATA["username"],
                password=C_USER_DATA["password"],
            )
            # Create Profile
            profile_ref = Profile.objects.create(
                company=admin_company_ref,
                user=user_ref,
                first_name=C_USER_DATA["name"]["first"],
                last_name=C_USER_DATA["name"]["last"],
                date_of_birth=C_USER_DATA["dob"],
                changedBy=C_USER_DATA["username"],
            )
        except Exception as e:
            raise Exception("User Creation Error !")
        super(MasterTestCase, self).setUp()

    def test_create_01(self):
        """
        Test creating a model instance.
        """
        self.assertTrue(True)

    def test_update_01(self):
        """
        Test updating a model instance.
        """
        self.assertTrue(True)

    def test_read_01(self):
        """
        Test checking the save method of a model.
        """
        self.assertTrue(True)

    def test_read_02(self):
        """
        Test the string representation of a model.
        """
        self.assertTrue(True)

    def test_delete_01(self):
        """
        Test soft deleting a model instance.
        """
        self.assertTrue(True)

    def test_delete_02(self):
        """
        Test forced deleting a model instance.
        """
        self.assertTrue(True)


class MasterAPIViewTest(APITestCase):
    """
    MasterAPIViewTest to provide a base class for API tests.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_reverse = reverse
        self.import_status = status

    def setUp(self):
        """
        Set up test data for API tests and authentication.
        """
        try:
            # Create Admin Company
            admin_company_ref = Company.objects.create(
                name="admin",
                changedBy=C_USER_DATA["username"],
            )
            # Create user
            user_ref = User.objects.create_user(
                username=C_USER_DATA["username"],
                password=C_USER_DATA["password"],
            )
            # Create Profile
            profile_ref = Profile.objects.create(
                company=admin_company_ref,
                user=user_ref,
                first_name=C_USER_DATA["name"]["first"],
                last_name=C_USER_DATA["name"]["last"],
                date_of_birth=C_USER_DATA["dob"],
                changedBy=C_USER_DATA["username"],
            )
        except Exception as e:
            raise Exception("User Creation Error !")

        credentials = "{}:{}".format(
            C_USER_DATA["username"],
            C_USER_DATA["password"],
        ).encode("utf-8")
        encoded_credentials = base64.b64encode(credentials)
        encoded_credentials = encoded_credentials.decode("utf-8")
        self.headers = {"Authorization": f"Basic {encoded_credentials}"}

        super(MasterAPIViewTest, self).setUp()

    def test_read_01(self):
        """
        Test OPTIONS request for the API.
        """
        self.assertTrue(True)

    def test_read_02(self):
        """
        Test GET request for the API.
        """
        self.assertTrue(True)

    def test_create_01(self):
        """
        Test POST request for creating a resource.
        """
        self.assertTrue(True)

    def test_create_02(self):
        """
        Test POST request with invalid data for creating a resource.
        """
        self.assertTrue(True)

    def test_update_01(self):
        """
        Test PUT request for updating a resource.
        """
        self.assertTrue(True)

    def test_delete_01(self):
        """
        Test DELETE request for deleting a resource.
        """
        self.assertTrue(True)
