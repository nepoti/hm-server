# Client
CLIENT_PLATFORMS = ['android']
CLIENT_MIN_VERSION = {'android': '0.3'}

# UserProfile fields
UserProfile_ALLOWED_KEYS = {'name': 30, 'gender': 20, 'country': 50, 'city': 200}

# Validation regex
REGEX_EMAIL = "^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}.]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$"
