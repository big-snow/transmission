#-*- coding: utf-8 -*-
import core

if __name__ == '__main__':
    drive = core.Drive('credential file path')
    results = drive.service.files().list(
            pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print 'No files found.'
    else:
        print 'Files:'
        for item in items:
            print '{0} ({1})'.format(item['name'], item['id'])
