#-*- coding: utf-8 -*-
'''
import 
'''
import util
import urllib2
from base64 import b64encode

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

class CustomError(Exception):
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
                raise CustomError('connection fail: missing user, passwd ')
        return sessionId

    def _req(self, tag, method, args):
        query = util.json_parser({'tag' : tag, 'method' : method, 'arguments' : args}, 'w')
        headers = {self._session_id_key : self._session_id_val}
        request = urllib2.Request(self._url, query, headers)
        res = self._http_opener.open(request)
        return util.json_parser(res.read().decode('utf-8'), 'r')

    def add_torrent(self, filepath, download_dir):
        args = {}
        args['metainfo'] = util.readFile(filepath, b64encoding=True)
        args['download_dir'] = download_dir
        return self._req('torrent', 'torrent-add', args)

class Drive:
    
    _scopes = ['https://www.googleapis.com/auth/drive']

    def __init__(self, certificate_path):
        credentials = service_account.Credentials.from_service_account_file(certificate_path, scopes=self._scopes)
        self._service = build('drive', 'v3', credentials=credentials)

    def _get_list(self, kind, name=None, parents_id=None):
        if kind:
            query = ''
            if kind == 'dir':
                query += 'mimeType = "application/vnd.google-apps.folder" '
            elif kind == 'file':
                query += 'mimeType != "application/vnd.google-apps.folder" '

            if name:
                query += 'and name = "' + name + '" '

            if parents_id:
                query += 'and parents = "' + parents_id + '" '

            rtn = self._service.files().list(q=query, spaces='drive').execute()    
            return rtn['files']
        else:
            return 

    def get_root_id(self, root_name):
        root = self._get_list(kind='dir', name=root_name)
        return root[0].get('id')

    def dir_walk(self, parents_id, parents_path, file_list):
        files = self._get_list(kind='file', parents_id=parents_id)
        
        if 0 < len(files):
            for f in files :
                dic = {'id':f['id'], 'name':f['name'], 'dir':parents_path}
                file_list.append(dic)

        dirs = self._get_list(kind='dir', parents_id=parents_id)

        if 0 < len(dirs):
            for d in dirs:
                self.dir_walk(d['id'], util.join_path(parents_path, d['name']), file_list)
        
        return file_list


    def file_download(self, file_id, download_dir):
        req = self._service.files().get_media(fileId=file_id)
        fio = util.getIO(download_dir, 'wb')
        with fio:                
            downloader = MediaIoBaseDownload(fio, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print "Download %d%%." % int(status.progress() * 100)
        
    
    
        
                                         

            
        