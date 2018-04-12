#-*- coding: utf-8 -*-

import os
import io
import json
from base64 import b64encode
from six import string_types

def fromJson(data):
    if isinstance(data, string_types):
        return json.loads(data)
    elif isinstance(data, file):
        return json.load(data)

def toJson(data, write_io=None):
    if write_io:
        return json.dump(data, write_io)
    else:
        return json.dumps(data)
    
def readFile_b64encoded(path):
    fio, data = None, None
    try:
        if os.path.isfile(path):
            fio = io.FileIO(path, 'rb')
            data = fio.read()
            return b64encode(data).decode('utf-8')
    except IOError :
        raise IOError()
    finally:
        if fio: fio.close()

def join(*args):
    rtn = '' 
    for arg in args:
        rtn = os.path.join(rtn, arg)
    return rtn

def fileIO(path, mode):
    return io.FileIO(path, mode)

def mkdirs(path):
    if os.path.isfile(path):
        path = os.path.dirname(path)
    if not os.path.isdir(path):
        os.makedirs(path)
        os.chmod(path, 0777)

def remove(path):
    if os.path.isfile(path):
        os.remove(path)