from redis import ConnectionPool

from .conf_parser import REDIS_SETTINGS


pool = ConnectionPool(
    host=REDIS_SETTINGS['host'],
    port=REDIS_SETTINGS['port'],
    db=int(REDIS_SETTINGS['db']),
    password=REDIS_SETTINGS['password']
)
