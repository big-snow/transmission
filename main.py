#-*- coding: utf-8 -*-

import util
from drive import Drive
from transmission import Transmission

def download(transmission, dirve, root_id, download_base):
    for file in drive.dir_walk(root_id):
        download_dir = util.join(download_base, file['dir'])
        download_path = util.join(download_dir, file['name'])

        util.mkdirs(download_dir)

        io_w = util.fileIO(download_path, 'wb')
        drive.download(file['id'], io_w)

        trans_result = transmission.add_torrent(download_path, download_dir)
        if trans_result and trans_result.get('result') == 'success':
            util.remove(download_path)
            drive.delete(file['id'])
        else:
            print trans_result

if __name__ == '__main__':   
    f = open('/home/test/git/transmission/settings_test.json')
    settings = util.fromJson(f)
    f.close()

    USER = settings['transmission']['user']
    PASSWD = settings['transmission']['passwd']
    
    CREDENTIAL_INIT = settings['dirve']['credential-init']
    CREDENTIAL_RETRIVE = settings['dirve']['credential-retrive']

    transmission = Transmission(USER, PASSWD)
    drive = Drive(CREDENTIAL_INIT,CREDENTIAL_RETRIVE)

    for folder in settings['download']:
        root_name = folder['drive-root']
        download_base = folder['download-base']
        root_id = drive.get_list(file=False, name=root_name)[0]['id']    
        
        download(transmission, drive, root_id, download_base)