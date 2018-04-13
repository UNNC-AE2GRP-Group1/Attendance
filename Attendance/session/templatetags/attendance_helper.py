from django import template

register = template.Library()

@register.simple_tag
def attendance_style(attendance, student_to_app_details):
    if attendance == None:
        return "unenrolled"
    else:
        ret = ""
        details = student_to_app_details.get(attendance.student.pk)
        if details != None:
            for detail in details:
                 if attendance.session.is_affected_by_application_detail(detail):
                     ret += "excused "
                     break
        ret += "absent " if not attendance.presented else "presented "
        if attendance.comment:
            ret += "commented "
    return ret
