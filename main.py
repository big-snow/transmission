#-*- coding: utf-8 -*-

import core


drive = core.Drive('/home/test/Desktop/secret.json')
result = drive.get_folder_list('1CSnlq1rd2e1wdUYfj3ph03zSrv8SkhIK')

for file in result.get('files', []):
    print '%s, (%s)' % (file['name'], file['id'])