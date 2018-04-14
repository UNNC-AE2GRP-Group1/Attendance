from django.test import TransactionTestCase, Client
from io import StringIO
from django.urls import reverse
import datetime
from dateutil.tz import tzlocal
import json

from session.models import Module, Session
from student.models import Student

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
        response = c.post(reverse('module_student_import', args=[pgp.pk]), { 'student_list_csv': student_csv })
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
        response = c.post(reverse('module_student_import', args=[pgp.pk]), { 'student_list_csv': student_csv })
        student_list2 = pgp.students.all().order_by('student_id')

        # data conflict, nothing is changed
        self.assertEqual(student_list2.count(), 3)
        self.assertEqual(student_list2[0].first_name, "Chris")
        self.assertEqual(student_list2[1].first_name, "Paul")
        self.assertEqual(student_list2[2].first_name, "First") # does not overwrite old record

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

    def test_taking_attendance(self):
        pgp = Module.objects.get(code="AE1PGP")

        session = Session.objects.create(module=pgp)

        pgp.students.bulk_create([
            Student(student_id="16510000", first_name="Hua", last_name="Li"),
            Student(student_id="16510001", first_name="Tai Man", last_name="Chan"),
            Student(student_id="16510002", first_name="Ivan", last_name="Horvat"),
        ])

        c = Client()

        response = c.post(reverse('session_taking_attendance', args=[session.pk]), json.dumps({
            "16510000":{"student_id":"16510000","first_name":"Hua","last_name":"Li","presented":True,"comment":""},
            "16510001":{"student_id":"16510001","first_name":"Tai Man","last_name":"Chan","presented":False,"comment":""},
            "16510002":{"student_id":"16510002","first_name":"Ivan","last_name":"Horvat","presented":True,"comment":""},
            "16510003":{"student_id":"16510003","first_name":"Jane","last_name":"Doe","presented":True,"comment":""},
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        session.refresh_from_db()
        attendees = session.attendee_set.prefetch_related('student').all().order_by('student__student_id')
        self.assertEqual(attendees.count(), 4)
        self.assertEqual(attendees[0].student.student_id, '16510000')
        self.assertEqual(attendees[0].presented, True)
        self.assertEqual(attendees[1].student.student_id, '16510001')
        self.assertEqual(attendees[1].presented, False)
        self.assertEqual(attendees[2].student.student_id, '16510002')
        self.assertEqual(attendees[2].presented, True)
        self.assertEqual(attendees[3].student.student_id, '16510003')
        self.assertEqual(attendees[3].presented, True)
        self.assertAlmostEqual(session.attendance_rate, 0.75)

        response = c.post(reverse('session_taking_attendance', args=[session.pk]), json.dumps({
            "16510000":{"student_id":"16510000","first_name":"Hua","last_name":"Li","presented":False,"comment":""},
            "16510001":{"student_id":"16510001","first_name":"Tai Man","last_name":"Chan","presented":True,"comment":""},
            "16510002":{"student_id":"16510002","first_name":"Ivan","last_name":"Horvat","presented":True,"comment":""},
            "16510003":{"student_id":"16510003","first_name":"Jane","last_name":"Doe","presented":True,"comment":""},
            "16510004":{"student_id":"16510004","first_name":" hello  bad name  ","last_name":"Doe","presented":True,"comment":"Bad"},
        }), content_type="application/json")
        self.assertEqual(response.status_code, 200)

        session.refresh_from_db()
        attendees = session.attendee_set.prefetch_related('student').all().order_by('student__student_id')
        self.assertEqual(attendees.count(), 5)
        self.assertEqual(attendees[0].student.student_id, '16510000')
        self.assertEqual(attendees[0].presented, False)
        self.assertEqual(attendees[1].student.student_id, '16510001')
        self.assertEqual(attendees[1].presented, True)
        self.assertEqual(attendees[2].student.student_id, '16510002')
        self.assertEqual(attendees[2].presented, True)
        self.assertEqual(attendees[3].student.student_id, '16510003')
        self.assertEqual(attendees[3].presented, True)
        self.assertEqual(attendees[4].student.student_id, '16510004')
        self.assertEqual(attendees[4].student.first_name, 'Hello Bad Name')
        self.assertEqual(attendees[4].student.last_name, 'Doe')
        self.assertEqual(attendees[4].presented, True)
        self.assertEqual(attendees[4].comment, "Bad")
        self.assertAlmostEqual(session.attendance_rate, 0.8)