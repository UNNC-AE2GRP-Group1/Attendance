from bridgekeeper import perms
from bridgekeeper.rules import is_staff
from .rules import *

perms['module.create'] = is_staff
perms['module.view'] = is_staff | is_convenor | is_teaching_assistant
perms['module.take_attendance'] = is_staff | is_convenor | is_teaching_assistant
perms['module.view_history'] = is_staff | is_convenor
perms['module.create_session'] = is_staff | is_convenor
perms['module.import_student'] = is_staff

perms['statistics.view'] = is_staff | is_senior_tutor
perms['application'] = is_staff | is_senior_tutor

perms['student.view'] = is_staff | is_senior_tutor
