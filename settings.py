import os

SECRET_KEY = 'cX\tD;K\xa5\x1e#\xc1(\xb6\x19}.\x87\xbem\x9flp\xec\xa2\xfb'
DEBUG = True
DB_USERNAME = 'skols75'
DB_PASSWORD = ''
BLOG_DATABASE_NAME = 'blog'
# For Cloud9
DB_HOST = os.getenv('IP', '0.0.0.0')
# mysql+pymsql://username:password@hostname/tablename
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOADED_IMAGES_DEST = '/home/ubuntu/workspace/flask_blog/static/images/'
UPLOADED_IMAGES_URL = '/static/images/'
