# 定义数据库信息
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/vjudge'
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_POOL_SIZE = 1000
SQLALCHEMY_MAX_OVERFLOW = -1
SQLALCHEMY_POOL_TIMEOUT = 120
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义flask信息
SECRET_KEY = '123456'
WHITELIST_UA = '123456'

# 定义打码平台信息
lianzhong_software_id = ''
lianzhong_software_secret = ''
lianzhong_username = ''
lianzhong_password = ''
