import os
import io
import json

def json_parser(data, mode):
    if mode == 'r':
        return json.loads(data)
    elif mode == 'w':
        return json.dumps(data)
    else:
        return
    
def readFile(path, b64encoding=False):
    fio, data = None, None
    try:
        if os.path.isfile(path):
            fio = io.FileIO(path, 'rb')
            data = fio.read()
            if b64encoding: 
                return b64encoding(data).decode('utf-8')
            else:
                return data
    except IOError :
        raise IOError()
    finally:
        if fio: fio.close()

def join_path(*args):
    rtn = '' 
    for arg in args:
        rtn = os.path.join(rtn, arg)
    return rtn

def getIO(path, mode):
    return io.FileIO(path, mode)

def curr_path():
    return os.getcwd()