from django.test import TransactionTestCase, Client
from io import StringIO
from django.urls import reverse

from session.models import Module

class ModuleViewTest(TransactionTestCase):

    def setUp(self):
        Module.objects.create(
            name="Programming Paradigms",
            code="AE1PGP",
            academic_year=2018
        )

    def test_upload_student_list_csv(self):
        """Test that the student list can be imported from a csv and won't
        overwrite existing information.
        """
        pgp = Module.objects.get(code="AE1PGP")

        c = Client()

        csv = StringIO(
            "6510000,Chris,Rudd\n"
            "6510001,Paul,Dempster\n"
            "6510002,First,Last\n"
        )
        # add students to module student list
        response = c.post(reverse('module-students', args=[pgp.pk]), { 'student_list_csv': csv })
        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 3)
        self.assertEqual(student_list[0].first_name, "Chris")
        self.assertEqual(student_list[1].first_name, "Paul")
        self.assertEqual(student_list[2].first_name, "First")

        csv = StringIO(
            "6510000,Chris,Rudd\n"
            "6510001,Paul,Dempster\n"
            "6510002,Hello,Last\n"
            "6510003,Ming,Xiao\n"
        )
        # todo: the test currently fails due to integrity violation on the uniqueness of student_id, this case should be dealt with by checking conflicts before insertion
        response = c.post(reverse('module-students', args=[pgp.pk]), { 'student_list_csv': csv })
        student_list2 = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list2.count(), 4)
        self.assertEqual(student_list2[0].first_name, "Chris")
        self.assertEqual(student_list2[1].first_name, "Paul")
        self.assertEqual(student_list2[2].first_name, "First") # does not overwrite old record
        self.assertEqual(student_list2[3].first_name, "Ming")

