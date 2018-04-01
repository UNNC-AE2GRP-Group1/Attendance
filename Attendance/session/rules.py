from bridgekeeper.rules import blanket_rule, ManyRelation, Is

from django.contrib.auth.models import User

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
