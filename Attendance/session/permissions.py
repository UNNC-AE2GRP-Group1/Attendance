from bridgekeeper import perms
from bridgekeeper.rules import is_staff
from .rules import *

perms['module.create'] = is_staff
perms['module.view'] = is_convenor | is_teaching_assistant | is_staff
perms['module.create_session'] = is_convenor
