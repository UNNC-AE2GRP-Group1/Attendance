from django import template

register = template.Library()

@register.simple_tag
def attendance_style(a):
    if a == None:
        return "unenrolled"
    else:
        ret = ""
        ret += "absent " if not a.presented else "presented "
        if a.comment:
            ret += "commented "
    return ret
