class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*s^'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'yotatestdb'

config = {
    'development': DevelopmentConfig
}