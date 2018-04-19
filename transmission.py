#-*- coding: utf-8 -*-

import util
import urllib2

class Transmission:

    _session_id_key = 'x-transmission-session-id'

    def __init__(self, ip, port, user, passwd):
        self._url = 'http://' + ip + ':' + port + '/transmission/rpc'
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
        return sessionId

    def _req(self, tag, method, args):
        query = util.toJson({'tag' : tag, 'method' : method, 'arguments' : args})
        headers = {self._session_id_key : self._session_id_val}
        request = urllib2.Request(self._url, query, headers)
        res = self._http_opener.open(request)
        return util.fromJson(res.read().decode('utf-8'))

    def add_torrent(self, filepath, download_dir):
        args = {}
        args['metainfo'] = util.readFile_b64encoded(filepath)
        args['download-dir'] = download_dir
        return self._req('torrent', 'torrent-add', args)