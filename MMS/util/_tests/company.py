# =====================================================================

from django.test import TestCase
from util._models.company import Company

# =====================================================================


class CompanyTestCase(TestCase):

    def setUp(self):
        self.model_ref = Company.objects.create(
            createdBy="tester",
            changedBy="tester",
            is_active=True,
        )

    def test_create_model_ref(self):
        self.assertEqual(self.model_ref.createdBy, "tester")
        self.assertTrue(self.model_ref.is_active)

    def test_update_model_ref(self):
        self.model_ref.changedBy = "tester2"
        self.model_ref.save()
        self.assertEqual(self.model_ref.changedBy, "tester2")

    def test_delete_model_ref(self):
        self.model_ref.delete()
        self.assertFalse(Company.objects.filter(id=self.model_ref.id).exists())

    def test_soft_delete(self):
        self.model_ref.delete()
        self.assertFalse(self.model_ref.is_active)

    def test_forced_delete(self):
        self.model_ref.delete(FORCED=True)
        self.assertFalse(Company.objects.filter(id=self.model_ref.id).exists())

    def test_check_save(self):
        result = self.model_ref.check_save()
        self.assertTrue(result[0])

    def test_str_representation(self):
        self.assertEqual(str(self.model_ref), "[X]" if self.model_ref.is_active else "[]")
