from django.test import TransactionTestCase, Client
from io import StringIO
from django.urls import reverse
import datetime
from dateutil.tz import tzlocal

from session.models import Module, Session

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

        student_csv = StringIO(
            "6510000,Chris,Rudd\n"
            "6510001,Paul,Dempster\n"
            "6510002,First,Last\n"
        )
        # add students to module student list
        response = c.post(reverse('module-student-import', args=[pgp.pk]), { 'student_list_csv': student_csv })
        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 3)
        self.assertEqual(student_list[0].first_name, "Chris")
        self.assertEqual(student_list[1].first_name, "Paul")
        self.assertEqual(student_list[2].first_name, "First")

        student_csv = StringIO(
            "6510000,Chris,Rudd\n"
            "6510001,Paul,Dempster\n"
            "6510002,Hello,Last\n"
            "6510003,Ming,Xiao\n"
        )
        # todo: the test currently fails due to integrity violation on the uniqueness of student_id, this case should be dealt with by checking conflicts before insertion
        response = c.post(reverse('module-student-import', args=[pgp.pk]), { 'student_list_csv': student_csv })
        student_list2 = pgp.students.all().order_by('student_id')

        # data conflict, nothing is changed
        self.assertEqual(student_list2.count(), 3)
        self.assertEqual(student_list2[0].first_name, "Chris")
        self.assertEqual(student_list2[1].first_name, "Paul")
        self.assertEqual(student_list2[2].first_name, "First") # does not overwrite old record

    def test_signature_sheet_availability(self):
        pgp = Module.objects.get(code="AE1PGP")

        # todo: test that signature sheet can only be downloaded after prepare the session

    def test_create_session(self):
        """Test that multiple sessions can be created by sepcifying the repeat time"""
        pgp = Module.objects.get(code="AE1PGP")

        c = Client()
        
        response = c.post(reverse('module_create_session', args=[pgp.pk]), {
            'time': '2018-04-15 16:00:00',
            'duration': '01:00:00',
            'place': 'SEB306',
            'type': Session.LAB,
            'repeat_for_weeks': '4',
        })
        self.assertEqual(response.status_code, 302) # redirect to index

        sessions = pgp.session_set.all().order_by('time')

        self.assertEqual(sessions.count(), 4)
        self.assertEqual(sessions[0].time, datetime.datetime(year=2018,month=4,day=15,hour=16,tzinfo=tzlocal()))
        self.assertEqual(sessions[1].time, datetime.datetime(year=2018,month=4,day=22,hour=16,tzinfo=tzlocal()))
        self.assertEqual(sessions[2].time, datetime.datetime(year=2018,month=4,day=29,hour=16,tzinfo=tzlocal()))
        self.assertEqual(sessions[3].time, datetime.datetime(year=2018,month=5,day=6,hour=16,tzinfo=tzlocal()))
