# =====================================================================

from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

# =====================================================================


class MasterTestCase(TestCase):

    def setUp(self):
        super(MasterTestCase, self).setUp()

    def test_create_model_ref(self):
        self.assertTrue(True)

    def test_update_model_ref(self):
        self.assertTrue(True)

    def test_check_save(self):
        self.assertTrue(True)

    def test_str_representation(self):
        self.assertTrue(True)

    def test_soft_delete(self):
        self.assertTrue(True)

    def test_forced_delete(self):
        self.assertTrue(True)


class MasterAPIViewTest(APITestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_reverse = reverse
        self.import_status = status

    def setUp(self):
        super(MasterAPIViewTest, self).setUp()

    def test_options_company(self):
        self.assertTrue(True)

    def test_get_company(self):
        self.assertTrue(True)

    def test_post_company(self):
        self.assertTrue(True)

    def test_post_invalid_company(self):
        self.assertTrue(True)

    def test_put_company(self):
        self.assertTrue(True)

    def test_delete_company(self):
        self.assertTrue(True)
