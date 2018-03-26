import django
from django.db import IntegrityError
from django.test import TestCase
from student.models import *

class StudentModelTest(TestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(StudentModelTest, cls).setUpClass()
        django.setup()

    def setUp(self):
        Student.objects.create(
            student_id="16510000",
            first_name="Hua",
            last_name="Li"
        )

    def test_unique_student(self):
        """Tests that two student cannot have the same student id
        """
        with self.assertRaises(IntegrityError):
            Student.objects.create(
                student_id="16510000",
                first_name="John",
                last_name="Doe"
            )
