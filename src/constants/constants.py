from os.path import abspath, dirname
from os import listdir
import json

SRC_PATH = dirname(dirname(__file__)).replace('\\.', '')


class PATH:
    DATABASE = SRC_PATH + '/Database'


class DATABASE:
    PATH = SRC_PATH + '/Database'
    LIST_DATABASES = lambda path: listdir(path)
    CREATE = json.dumps([])





