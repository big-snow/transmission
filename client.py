#-*- coding: utf-8 -*-
import urllib2
import json
from os.path import isfile
from base64 import b64encode, b64decode

DEFAULT_URL = 'http://localhost:9091/transmission/rpc'
SESSION_ID_KEY = 'x-transmission-session-id'
    
class TransmissionError(Exception):
    def __init__(self, msg=''):
        Exception.__init__(self)
        self.msg = msg
    def __str__(self):
        return self.msg

class Client:
    def __init__(self, user, passwd):
        self._url = DEFAULT_URL
        self._http_opener = self._getOpener(self._url, user, passwd)
        self._session_id = self._getSessionId(self._http_opener, self._url)
        self._seq = 0
    
    def _getOpener(self, url, user, passwd):
        passwdMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwdMgr.add_password(None, url, user, passwd)
        opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passwdMgr))
        return opener

    def _getSessionId(self, opener, url):
        sessionId = ''
        try:
            opener.open(url)
        except urllib2.HTTPError as err:
            if err.code == 409:
                for key in err.headers.keys():
                    if key.lower() == SESSION_ID_KEY:
                        sessionId = err.headers[key]
            else:
                raise TransmissionError('connection fail: missing user, passwd ')
        return sessionId

    def _req(self, method, args):
        self._seq += 1
        query = json.dumps({'tag':self._seq, 'method':method, 'arguments':args})
        headers = {SESSION_ID_KEY:self._session_id}
        request = urllib2.Request(self._url, query, headers)

        res = self._http_opener.open(request)
        return json.loads(res.read().decode('utf-8'))



    def add_torrent(self, filepath):
        torrentData = readFile(filepath)
        if torrentData:
            args = {'metainfo' : torrentData}
            return self._req('torrent-add', args)
        else:
            raise TransmissionError('there is no file')

def readFile(path):
    data = None
    if isfile(path):
        f = open(path, 'rb')
        data = f.read()
        f.close()
        data = b64encode(data).decode('utf-8')
    return data

try:
    a = Client('torrent', 'torrent')
    result = a.add_torrent('/home/test/Desktop/torrent.torrent')
    print result['result']
except TransmissionError as err:
    print err
