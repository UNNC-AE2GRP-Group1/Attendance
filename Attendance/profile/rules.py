from bridgekeeper.rules import blanket_rule

@blanket_rule
def is_senior_tutor(user):
    return user.profile.primary_role == 'ST'
