#-*- coding: utf-8 -*-
'''
import 
'''
import os
import json
import urllib2
import httplib2

from base64 import b64encode, b64decode
from googleapiclient.discovery import build
from google.oauth2 import service_account

'''
method
'''
def readFile(path):
    data = None
    if os.path.isfile(path):
        f = open(path, 'rb')
        data = f.read()
        f.close()
        data = b64encode(data).decode('utf-8')
    return data

'''
class
'''
class TransmissionError(Exception):
    def __init__(self, msg=''):
        Exception.__init__(self)
        self.msg = msg
    def __str__(self):
        return self.msg

class Transmission:

    _url =  'http://localhost:9091/transmission/rpc'
    _session_id_key = 'x-transmission-session-id'

    def __init__(self, user, passwd):
        self._http_opener = self._getOpener(self._url, user, passwd)
        self._session_id_val = self._getSessionId(self._http_opener, self._url)
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
                    if key.lower() == self._session_id_key:
                        sessionId = err.headers[key]
            else:
                raise TransmissionError('connection fail: missing user, passwd ')
        return sessionId

    def _req(self, method, args):
        self._seq += 1
        query = json.dumps({'tag' : self._seq, 'method' : method, 'arguments' : args})
        headers = {self._session_id_key : self._session_id_val}
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

class Drive:
    
    _scopes = ['https://www.googleapis.com/auth/drive.metadata']

    def __init__(self, secret_path):
        credentials = service_account.Credentials.from_service_account_file(secret_path, scopes=self._scopes)
        self._service = build('drive', 'v3', credentials=credentials)

    def get_folder_list(self, parents_id=None):
        query = ''
        query += 'mimeType = "application/vnd.google-apps.folder" '
        if parents_id:
            query += 'and parents = "' + str(parents_id) + '"'
        print query
        rtn =   self._service.files().list(q=query, spaces='drive').execute()
        return rtn
        
                                         

            
        