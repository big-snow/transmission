#-*- coding: utf-8 -*-
import core
import util
from subprocess import call

if __name__ == '__main__':
    conf = util.json_parser(util.readFile(util.join_path(os.getcwd(), 'settings.json')))

    transmission_conf = conf.get('transmission')
    drive_conf = conf.get('google_drive')

    drive = Drive(drive_conf['certificate_path'])
    root_id = drive.get_root_id(drive_conf['root_dir_name'])
    file_list = drive.dir_walk(root_id, '/', list())

    for file in file_list:
        download_dir = os.path.join(transmission_conf['base_dir'], file['dir'])
        print download_dir

        #drive.file_download(file['id'], file['path'])

    



#print torrent


# try:
#     transmission = core.Transmission('torrent', 'torrent')
#     drive = core.Drive('/home/test/Desktop/secret.json')
#     rootDir = drive.get_list(kind='dir', param={'name':'torrent'}).get('files', [])[0]
#     files = drive.get_list(kind='file', param={'parents_id':rootDir.get('id')}).get('files', [])
#     for file in files:
#         print '%s : %s' % (file.get('name'), file.get('id'))
#         drive.get_file(file.get('id'))
#         print transmission.add_torrent('/home/test/git/transmission/real.torrent')
    
    
        

# except:
#     pass    