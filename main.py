#-*- coding: utf-8 -*-

import util
from drive import Drive
from transmission import Transmission

CREDENTIAL_INIT = '/home/test/git/credential/credential_init.json'
CREDENTIAL_RETRIVE = '/home/test/git/credential/credential_retrive.json'

TRANSMISSION_USER = 'torrent'
TRANSMISSION_PASSWD = 'torrent'

DRIVE_DOWNLOAD_PATH = '/home/test/git/temp'
TRANSMISSION_DOWNLOAD_PATH = '/home/test/download'

if __name__ == '__main__':
    trans = Transmission(TRANSMISSION_USER, TRANSMISSION_PASSWD)
    drive = Drive(CREDENTIAL_INIT,CREDENTIAL_RETRIVE)

    root_id = drive.get_list(file=False, name='transmission')[0]['id']

    for file in drive.dir_walk(root_id):
        file_id = file['id']

        drive_download_path = util.join(DRIVE_DOWNLOAD_PATH, file['name'])
        util.mkdirs(drive_download_path)

        io_w = util.fileIO(drive_download_path, 'wb')
        drive.download(file_id, io_w)

        trans_download_dir = util.join(TRANSMISSION_DOWNLOAD_PATH, file['dir'])
        util.mkdirs(trans_download_dir)

        trans_result = trans.add_torrent(drive_download_path, trans_download_dir)
        if trans_result.get('result'):
            drive.delete(file_id)
        else:
            pass

    util.delete(DRIVE_DOWNLOAD_PATH)


            
