import django
from django.test import TransactionTestCase
from django.db import IntegrityError
from datetime import date, timedelta, datetime
from django.utils import timezone
import csv
from io import StringIO
from tzlocal import get_localzone

from session.models import Module, Session, Attendee
from student.models import Student
from absence_form.models import Detail

# TODO: Configure your database in settings.py and sync before running tests.

class ModuleWorkflowTest(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        # this is missing from the VS template but is required to run the tests.
        super(ModuleWorkflowTest, cls).setUpClass()
        django.setup()

    def setUp(self):
        Student.objects.create(student_id="16510000", first_name="Hua", last_name="Li")
        Student.objects.create(student_id="16510001", first_name="Tai Man", last_name="Chan")
        Student.objects.create(student_id="16510002", first_name="Ivan", last_name="Horvat")
        Student.objects.create(student_id="16510003", first_name="Jane", last_name="Doe")

        pgp = Module.objects.create(
            name="Programming Paradigms",
            code="AE1PGP",
            academic_year=2018
        )
        pgp.students.add(Student.objects.get(student_id="16510000"))
        pgp.students.add(Student.objects.get(student_id="16510001"))
        pgp.students.add(Student.objects.get(student_id="16510002"))
        pgp.students.add(Student.objects.get(student_id="16510003"))

    def test_batch_import_student_list(self):
        pgp = Module.objects.get(code="AE1PGP")

        # no conflicts
        student_csv = StringIO(
            "16510004,Chris,Rudd\n"
            "16510005,Paul,Dempster\n"
            "16510006,Hello,Last\n"
            "16510007,Ming,Xiao\n"
        )
        student_reader = csv.reader(student_csv, delimiter=',')
        conflict = pgp.batch_enroll_from_csv(student_reader)
        self.assertFalse(conflict)

        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 8)
        self.assertEqual(student_list[0].first_name, "Hua")
        self.assertEqual(student_list[1].first_name, "Tai Man")
        self.assertEqual(student_list[2].first_name, "Ivan")
        self.assertEqual(student_list[3].first_name, "Jane")
        self.assertEqual(student_list[4].first_name, "Chris")
        self.assertEqual(student_list[5].first_name, "Paul")
        self.assertEqual(student_list[6].first_name, "Hello")
        self.assertEqual(student_list[7].first_name, "Ming")

        # conflict
        student_csv = StringIO(
            "16510004,Wow,Rudd\n"
            "16510006,Awesome,Last\n"
            "16510007,Ming,Xiao\n"
        )
        student_reader = csv.reader(student_csv, delimiter=',')
        conflict = pgp.batch_enroll_from_csv(student_reader)
        self.assertEqual(len(conflict), 2)

        # no changes
        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 8)
        self.assertEqual(student_list[0].first_name, "Hua")
        self.assertEqual(student_list[1].first_name, "Tai Man")
        self.assertEqual(student_list[2].first_name, "Ivan")
        self.assertEqual(student_list[3].first_name, "Jane")
        self.assertEqual(student_list[4].first_name, "Chris")
        self.assertEqual(student_list[5].first_name, "Paul")
        self.assertEqual(student_list[6].first_name, "Hello")
        self.assertEqual(student_list[7].first_name, "Ming")

        # identical students remain
        student_csv = StringIO(
            "16510004,Chris,Rudd\n"
            "16510005,Paul,Dempster\n"
            "16510007,Ming,Xiao\n"
        )
        student_reader = csv.reader(student_csv, delimiter=',')
        conflict = pgp.batch_enroll_from_csv(student_reader)
        self.assertFalse(conflict)

        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 8)
        self.assertEqual(student_list[0].first_name, "Hua")
        self.assertEqual(student_list[1].first_name, "Tai Man")
        self.assertEqual(student_list[2].first_name, "Ivan")
        self.assertEqual(student_list[3].first_name, "Jane")
        self.assertEqual(student_list[4].first_name, "Chris")
        self.assertEqual(student_list[5].first_name, "Paul")
        self.assertEqual(student_list[6].first_name, "Hello")
        self.assertEqual(student_list[7].first_name, "Ming")

    def test_add_student_list(self):
        """Tests that students can be uniquely added to a module
        """
        pgp = Module.objects.get(code="AE1PGP")

        # fail silently
        pgp.students.add(Student.objects.get(student_id="16510003"))

        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 4)
        self.assertEqual(student_list[0].first_name, "Hua")
        self.assertEqual(student_list[1].first_name, "Tai Man")
        self.assertEqual(student_list[2].first_name, "Ivan")
        self.assertEqual(student_list[3].first_name, "Jane")

    def test_attendance_rates(self):
        """
        The attendance rate of a module is the average of those of finished
        sessions whose attendance rate are calculated.
        """
        pgp = Module.objects.get(code="AE1PGP")
        self.assertEqual(pgp.attendance_rate, None)

        # session 1
        session = pgp.session_set.create()
        session.attendee_set.add(Attendee.objects.create(session=session, student=Student.objects.get(student_id='16510000'), presented=True))
        session.attendee_set.add(Attendee.objects.create(session=session, student=Student.objects.get(student_id='16510001'), presented=True))
        session.attendee_set.add(Attendee.objects.create(session=session, student=Student.objects.get(student_id='16510002'), presented=True))
        session.attendee_set.add(Attendee.objects.create(session=session, student=Student.objects.get(student_id='16510003'), presented=False))
        session.update_attendance_rate()
        pgp.update_attendance_rate()

        self.assertAlmostEqual(session.attendance_rate, 0.75)
        self.assertAlmostEqual(pgp.attendance_rate, 0.75)

        # session 2
        Student.objects.create(student_id="16510004", first_name="Paul", last_name="Dave")

        session = pgp.session_set.create()
        session.attendee_set.bulk_create([
            Attendee(session=session, student=Student.objects.get(student_id='16510000'), presented=True),
            Attendee(session=session, student=Student.objects.get(student_id='16510001'), presented=True),
            Attendee(session=session, student=Student.objects.get(student_id='16510002'), presented=True),
            Attendee(session=session, student=Student.objects.get(student_id='16510003'), presented=False),
            Attendee(session=session, student=Student.objects.get(student_id='16510004'), presented=False),
        ])
        session.update_attendance_rate()
        pgp.update_attendance_rate()

        self.assertAlmostEqual(session.attendance_rate, 0.6)
        self.assertAlmostEqual(pgp.attendance_rate, 0.675)

        # session 3
        session = pgp.session_set.create()
        self.assertAlmostEqual(session.attendance_rate, None)
        self.assertAlmostEqual(pgp.attendance_rate, 0.675)

    def test_session_affected_by_application(self):
        """Tests that application influence is correctly determined"""
        pgp = Module.objects.get(code="AE1PGP")
        fake_pgp = Module.objects.create(
            name="Programming Paradigms",
            code="AE1PGP",
            academic_year=2018
        )
        session = pgp.session_set.create(
            time = datetime(2018, 4, 1, 12,0,tzinfo=get_localzone()),
            duration=timedelta(hours=1)
        )

        # full coverage
        detail = Detail(
            module=pgp,
            from_date=datetime(2018,3,29,tzinfo=get_localzone()),
            to_date=datetime(2018,4,2,tzinfo=get_localzone()),
        )
        self.assertTrue(session.is_affected_by_application_detail(detail))

        # fake module
        detail = Detail(
            module=fake_pgp,
            from_date=datetime(2018,3,29,tzinfo=get_localzone()),
            to_date=datetime(2018,4,2,tzinfo=get_localzone()),
        )
        self.assertFalse(session.is_affected_by_application_detail(detail))

        # ends in middle
        detail = Detail(
            module=pgp,
            from_date=datetime(2018,3,29,tzinfo=get_localzone()),
            to_date=datetime(2018,4,1,12,30,tzinfo=get_localzone()),
        )
        self.assertTrue(session.is_affected_by_application_detail(detail))

        # starts in middle
        detail = Detail(
            module=pgp,
            from_date=datetime(2018,4,1,12,30,tzinfo=get_localzone()),
            to_date=datetime(2018,4,1,2,tzinfo=get_localzone()),
        )
        self.assertTrue(session.is_affected_by_application_detail(detail))

        # before start
        detail = Detail(
            module=pgp,
            from_date=datetime(2018,3,1,12,30,tzinfo=get_localzone()),
            to_date=datetime(2018,4,1,11,59,tzinfo=get_localzone()),
        )
        self.assertFalse(session.is_affected_by_application_detail(detail))

        # after start
        detail = Detail(
            module=pgp,
            from_date=datetime(2018,4,1,13,1,tzinfo=get_localzone()),
            to_date=datetime(2018,5,1,12,30,tzinfo=get_localzone()),
        )
        self.assertFalse(session.is_affected_by_application_detail(detail))
