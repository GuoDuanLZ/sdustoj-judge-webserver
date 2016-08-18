# coding:utf-8

from configparser import ConfigParser

config = ConfigParser()
config.read('sdustoj_server.conf')


def get_config(name):
    ret = dict()
    items = config.items(name)

    for i, j in items:
        ret[i] = j

    return ret


POSTGRESQL_SETTINGS = get_config('postgresql')
MONGODB_SETTINGS = get_config('mongodb')
REDIS_SETTINGS = get_config('redis')

GLOBAL_SETTINGS = get_config('global')
TEST_DATA_READ_MAX = int(GLOBAL_SETTINGS['testdata_readmax'])
MAX_OLEN = int(GLOBAL_SETTINGS['max_output_length'])
