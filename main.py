#-*- coding: utf-8 -*-
import core
from subprocess import call

try:
    transmission = core.Transmission('torrent', 'torrent')
    drive = core.Drive('/home/test/Desktop/secret.json')
    rootDir = drive.get_list(kind='dir', param={'name':'torrent'}).get('files', [])[0]
    files = drive.get_list(kind='file', param={'parents_id':rootDir.get('id')}).get('files', [])
    for file in files:
        print '%s : %s' % (file.get('name'), file.get('id'))
        drive.get_file(file.get('id'))
        print transmission.add_torrent('/home/test/git/transmission/real.torrent')
    
    
        

except:
    pass    