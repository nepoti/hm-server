# Client
CLIENT_PLATFORMS = ['android']
CLIENT_MIN_VERSION = {'android': '0.3'}

# UserProfile fields
UserProfile_ALLOWED_KEYS = {'name': 30, 'profile_image': 200, 'gender': 20, 'country': 50, 'city': 200, 'about': 100}

# Image previews
UserProfile_PREVIEW_SIZE = (200, 200)
POST_PREVIEW_SIZE = (200, 200)
COMMENT_PREVIEW_SIZE = (200, 200)

# Requests limits
REQUEST_MAX_FOLLOWING = 20
REQUEST_MAX_FOLLOWERS = 20
REQUEST_MAX_POSTS = 10
REQUEST_MAX_COMMENTS = 10
REQUEST_MAX_LIKES = 10

# Post constants
POST_MAX_TEXT_LENGTH = 1000
POST_MAX_PHOTOS = 10
POST_MAX_LOCATIONS = 10

# PostComment constants
COMMENT_MAX_TEXT_LENGTH = 500
COMMENT_MAX_PHOTOS = 10
COMMENT_MAX_LOCATIONS = 10

# S3
S3_REGION = 'eu-central-1'  # Frankfurt
S3_HOST = 's3.eu-central-1.amazonaws.com'  # special host for Frankfurt
S3_BUCKET = 'thehealthme'
S3_MAX_FILE_SIZE = 5*1024*1024  # 5 MB
S3_MAX_URL_GENERATE_ATTEMPTS = 10
S3_URL_EXPIRATION_TIME = 3600

# Validation regex
REGEX_USERNAME = "^([a-zA-Z0-9_@\+\.\-]{1,30})$"
REGEX_EMAIL = "^[a-zA-Z0-9_\-!\$&\*\-=\^`\|~%'\+\/\?_{}.]*@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,6}$"
