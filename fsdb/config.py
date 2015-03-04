from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import open
from builtins import int
from builtins import oct
from builtins import str, bytes
from future import standard_library
standard_library.install_aliases()
import json

CONFIG_SECTION = "fsdb"
DEFAULT_MODE = "0770"
DEFAULT_DEEP = 3
ACCEPTED_HASH_ALG = ['md5', 'sha', 'sha1', 'sha224', 'sha2', 'sha256', 'sha384', 'sha512']
DEFAULT_HASH_ALG = 'sha1'

TAG = "fsdb_config"


def normalizeConf(oldConf):

    if not isinstance(oldConf, dict):
        raise TypeError(TAG+": bad format for config file, not a `dict`")

    conf = oldConf.copy()

    if 'mode' not in conf:
        conf['mode'] = DEFAULT_MODE
    elif not isinstance(conf['mode'], str):
        raise TypeError(TAG+": `mode` must be a string")

    conf['mode'] = int(conf['mode'], 8)

    if 'deep' not in conf:
        conf['deep'] = DEFAULT_DEEP
    elif not isinstance(conf['deep'], int):
        raise TypeError(TAG+": `deep` must be an int")
    elif conf['deep'] < 0:
        raise ValueError(TAG+": `deep` must be a positive number")

    if 'hash_alg' not in conf:
        conf['hash_alg'] = DEFAULT_HASH_ALG
    elif not isinstance(conf['hash_alg'], str):
        raise TypeError(TAG+": `hash_alg` must be a string")
    elif conf['hash_alg'] not in ACCEPTED_HASH_ALG:
        raise ValueError(TAG+": `hash_alg` must be one of "+str(ACCEPTED_HASH_ALG))

    return conf


def loadConf(configPath):
    print(configPath)
    with open(configPath, 'r', encoding='utf-8') as configFile:
        content = configFile.read()
        conf = json.loads(content)

    return normalizeConf(conf)


def writeConf(configPath, conf):
    if not isinstance(conf, dict):
        raise TypeError(TAG+": bad format for config file, not a `dict`")

    mConf = conf.copy()

    if 'mode' in mConf:
        mConf['mode'] = str(oct(mConf['mode']))

    json_content = json.dumps(mConf, indent=4)
    if isinstance(json_content, bytes):
        json_content = json_content.decode('utf-8')
    with open(configPath, 'w', encoding='utf-8') as outfile:
        outfile.write(json_content)


def getDefaultConf():
    return {'mode': DEFAULT_MODE, 'deep': DEFAULT_DEEP, 'hash_alg': DEFAULT_HASH_ALG}
