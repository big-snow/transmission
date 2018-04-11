import httplib2
import argparse

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.tools import argparser, run_flow
from oauth2client.file import Storage

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly','https://www.googleapis.com/auth/drive.file']

class Drive():
    def __init__(self, credential_init, credential_retrive):
        credential = self._get_credentail(credential_init, credential_retrive)
        self.service = build('drive', 'v3', http=credential.authorize(httplib2.Http()))

    def _get_credentail(self, credential_init, credential_retrive):
        storage = Storage(credential_retrive)
        credential = storage.get()
        if not credential or credential.invalid:
            flags = argparse.ArgumentParser(parents=[argparser]).parse_args()
            flow = flow_from_clientsecrets(credential_init, scope=SCOPES)
            credential = run_flow(flow, storage, flags)
        return credential
    
if __name__ == '__main__':
    d = Drive('/home/test/git/credential/credential_init.json','/home/test/git/credential/credential_retrive.json')
        
