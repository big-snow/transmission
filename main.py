#-*- coding: utf-8 -*-

import util
from drive import Drive
from transmission import Transmission

if __name__ == '__main__':   
    settings = util.fromJson(open('/home/test/git/transmission/settings_test.json'))

    USER = settings['TRANSMISSION_USER']
    PASSWD = settings['TRANSMISSION_PASSWD']
    DOWNLOAD_PATH = settings['DOWNLOAD_PATH']

    CREDENTIAL_INIT = settings['DRIVE_CREDENTIAL_INIT']
    CREDENTIAL_RETRIVE = settings['DRIVE_CREDENTIAL_RETRIVE']
    ROOT_NAME = settings['ROOT_NAME']

    trans = Transmission(USER, PASSWD)
    drive = Drive(CREDENTIAL_INIT,CREDENTIAL_RETRIVE)

    root_id = drive.get_list(file=False, name=ROOT_NAME)[0]['id']

    for file in drive.dir_walk(root_id):
        download_dir = util.join(DOWNLOAD_PATH, file['dir'])
        download_path = util.join(download_dir, file['name'])

        util.mkdirs(download_dir)

        io_w = util.fileIO(download_path, 'wb')
        drive.download(file['id'], io_w)

        trans_result = trans.add_torrent(download_path, download_dir)
        if trans_result and trans_result.get('result'):
            util.remove(download_path)
            drive.delete(file['id'])
        else:
            pass