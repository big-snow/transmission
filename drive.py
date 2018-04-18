# -*- coding = utf-8 -*-

import util
import httplib2
import argparse

#from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import argparser, run_flow
from oauth2client.file import Storage
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


class Drive():

    _scopes = ['https://www.googleapis.com/auth/drive']

    def __init__(self, credential_init, credential_retrive):
        credential = self._get_credentail(credential_init, credential_retrive)
        self.service = build('drive', 'v3', http=credential.authorize(httplib2.Http()))

    def _get_credentail(self, credential_init, credential_retrive):
        storage = Storage(credential_retrive)
        credential = storage.get()
        if not credential or credential.invalid:
            flags = argparse.ArgumentParser(parents=[argparser]).parse_args()
            flow = flow_from_clientsecrets(credential_init, scope=self._scopes)
            credential = run_flow(flow, storage, flags)
        return credential

    def get_list(self, file=True, id=None, name=None, parents_id=None):
        query = ''
        if file:
            query += 'mimeType != "application/vnd.google-apps.folder" '
        else:
            query += 'mimeType = "application/vnd.google-apps.folder" '
        if id:
            query += 'and id = "' + id + '" '
        if name:
            query += 'and name = "' + name + '" '
        if parents_id:
            query += 'and parents = "' + parents_id + '" '
        
        return self.service.files().list(spaces='drive', q=query).execute()['files']

    def dir_walk(self, root_dir_id):
        files = list()

        def recursive_func(root_dir_id, root_path, files):
            sub_files = self.get_list(file=True, parents_id=root_dir_id)
            for f in sub_files:
                m = {'id':f['id'], 'name':f['name'], 'dir':root_path}
                files.append(m)

            sub_dirs = self.get_list(file=False, parents_id=root_dir_id)
            for d in sub_dirs:
                recursive_func(d['id'], util.join(root_path, d['name']), files)

            return files

        return recursive_func(root_dir_id, '', files)
    
    def download(self, file_id, write_io):
        try:
            req = self.service.files().get_media(fileId=file_id)
            downloader  = MediaIoBaseDownload(write_io, req)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print "Download %d%%." % int(status.progress() * 100)
        except IOError:
            raise
        finally:
            if write_io: write_io.close()
    
    def delete(self, file_id):
        self.service.files().delete(fileId=file_id).execute()