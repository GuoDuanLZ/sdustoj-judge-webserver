from mongoengine import connect

from .conf_parser import MONGODB_SETTINGS


connect(
    host=MONGODB_SETTINGS['host'],
    authentication_source=MONGODB_SETTINGS['authdb'],
    db=MONGODB_SETTINGS['db'],
    username=MONGODB_SETTINGS['user'],
    password=MONGODB_SETTINGS['password']
)
