import django
from django.test import TransactionTestCase
from session.models import Module, Session
from student.models import Student
from django.db import IntegrityError
from datetime import date, timedelta
from django.utils import timezone

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
        Student.objects.create(student_id="20001001", first_name="Jane", last_name="Doe")

        pgp = Module.objects.create(
            name="Programming Paradigms",
            code="AE1PGP",
            academic_year=2018
        )
        pgp.enroll_student(Student.objects.get(student_id="16510000"))
        pgp.enroll_student(Student.objects.get(student_id="16510001"))
        pgp.enroll_student(Student.objects.get(student_id="16510002"))
        pgp.enroll_student(Student.objects.get(student_id="20001001"))

    def test_add_student_list(self):
        """Tests that students can be uniquely added to a module
        """
        pgp = Module.objects.get(code="AE1PGP")

        with self.assertRaises(IntegrityError):
            pgp.enroll_student(Student.objects.get(student_id="20001001"))

        student_list = pgp.students.all().order_by('student_id')

        self.assertEqual(student_list.count(), 4)
        self.assertEqual(student_list[0].first_name, "Hua")
        self.assertEqual(student_list[1].first_name, "Tai Man")
        self.assertEqual(student_list[2].first_name, "Ivan")
        self.assertEqual(student_list[3].first_name, "Jane")

    def test_prepare_session_copies_student_list(self):
        """Tests that the student list is copied as attendee list
        """
        pgp = Module.objects.get(code="AE1PGP")
        session = pgp.session_set.create()
        session.prepare()

        attendee_list = session.attendee_set.all().order_by('student_id')
        attendee_list.prefetch_related('student')

        self.assertEqual(attendee_list.count(), 4)
        self.assertEqual(attendee_list[0].student.first_name, "Hua")
        self.assertEqual(attendee_list[1].student.first_name, "Tai Man")
        self.assertEqual(attendee_list[2].student.first_name, "Ivan")
        self.assertEqual(attendee_list[3].student.first_name, "Jane")

    def test_attendance_rates(self):
        """
        The attendance rate of a module is the average of those of finished
        sessions whose attendance rate are calculated.
        """
        pgp = Module.objects.get(code="AE1PGP")
        self.assertEqual(pgp.attendance_rate, None)

        # session 1
        session = pgp.session_set.create()
        session.prepare()
        for index, attendee in enumerate(session.attendee_set.all()):
            if index == 3:
                break
            attendee.presented = True
            attendee.save()
        session.attendance_recorded = True
        session.calculate_attendance_rate()
        session.save()
        pgp.calculate_attendance_rate()
        pgp.save()

        self.assertAlmostEqual(session.attendance_rate, 0.75)
        self.assertAlmostEqual(pgp.attendance_rate, 0.75)

        # session 2
        session = pgp.session_set.create()
        session.prepare()
        for index, attendee in enumerate(session.attendee_set.all()):
            if index == 2:
                break
            attendee.presented = True
            attendee.save()
        session.attendance_recorded = True
        session.calculate_attendance_rate()
        session.save()
        pgp.calculate_attendance_rate()
        pgp.save()

        self.assertAlmostEqual(session.attendance_rate, 0.5)
        self.assertAlmostEqual(pgp.attendance_rate, 0.625)

        # session 3
        session = pgp.session_set.create()
        self.assertAlmostEqual(session.attendance_rate, None)
        self.assertAlmostEqual(pgp.attendance_rate, 0.625)

    def test_session_status(self):
        pgp = Module.objects.get(code="AE1PGP")

        # set time on 1 hour in the future so it won't start immediately
        session = pgp.session_set.create(
            time=timezone.now() + timedelta(hours=1),
            duration=timedelta(hours=2)
        )
        self.assertEqual(session.get_status(), Session.SCHEDULED)

        session.prepare()
        self.assertEqual(session.get_status(), Session.PENDING)

        session.time = timezone.now() - timedelta(hours=1) 
        self.assertEqual(session.get_status(), Session.IN_PROGRESS)

        with self.assertRaises(AssertionError):
            session.cancel()

        session.time = timezone.now() - timedelta(hours=3) 
        self.assertEqual(session.get_status(), Session.FINISHED)

        with self.assertRaises(AssertionError):
            session.cancel()
