"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import django
from django.test import TestCase
from session.models import *

# TODO: Configure your database in settings.py and sync before running tests.

class ModuleAttendanceRateTest(TestCase):
    """Tests for the application views."""

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(ModuleAttendanceRateTest, cls).setUpClass() 
        django.setup()

    def setUp(self):
        Module.objects.create(
            name="Programmng Paradigms",
            code="AE1PGA",
            academic_year=2018
        )
        pga = Module.objects.get(code="AE1PGA")
        pga.session_set.create(attendance_rate=0.35)
        pga.session_set.create(attendance_rate=0.55)
        pga.session_set.create(attendance_rate=0.9)
        pga.session_set.create()

    def test_sum_only_sessions_with_record(self):
        """
        The attendance rate of a module is the average of those of finished
        sessions whose attendance rate are calculated.
        """
        pga = Module.objects.get(code="AE1PGA")
        self.assertEqual(pga.attendance_rate, None)
        pga.update_attendance_rate()
        self.assertAlmostEqual(pga.attendance_rate, 0.6)
