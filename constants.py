# Client
CLIENT_PLATFORMS = ['android']
CLIENT_MIN_VERSION = {'android': '0.3'}

# UserProfile fields
UserProfile_ALLOWED_KEYS = {'name': 30, 'gender': 20, 'country': 50, 'city': 200}
UserProfile_BLOOD_CHOICES = (1, 2, 3, 4, -1, -2, -3, -4)

# Validation regex
REGEX_EMAIL = "^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}.]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$"
PHONE_PREFIXES = ('38',)


def is_valid_phone(phone):
    if len(phone) != 12 or not phone.isdigit():
        return False
    if phone[:2] not in PHONE_PREFIXES:
        return False
    return True
