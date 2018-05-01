from bridgekeeper.rules import blanket_rule, ManyRelation, Is

from django.contrib.auth.models import User

from profile.models import Profile

# check against Module
is_convenor = ManyRelation(
    'convenors',
    'convenors',
    User,
    Is(lambda user: user)
)

# check against Module
is_teaching_assistant = ManyRelation(
    'assistants',
    'assistants',
    User,
    Is(lambda user: user)
)

@blanket_rule
def is_senior_tutor(user):
    return user.profile.primary_role == Profile.SENIOR_TUTOR
