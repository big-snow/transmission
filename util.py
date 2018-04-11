import os
import io
import json
from base64 import b64encode

def json_parser(data, mode):
    if mode == 'r':
        return json.loads(data)
    elif mode == 'w':
        return json.dumps(data)
    else:
        return
    
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
        fio.close()

def join(*args):
    rtn = '' 
    for arg in args:
        rtn = os.path.join(rtn, arg)
    return rtn

def getIO(path, mode):
    return io.FileIO(path, mode)

def curr_path():
    return os.getcwd()