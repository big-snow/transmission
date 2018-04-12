#-*- coding: utf-8 -*-

import util
from drive import Drive
from transmission import Transmission

if __name__ == '__main__':   
    settings = util.fromJson(open('/home/test/git/transmission/settings.json'))

    trans_conf = settings['transmission']
    drive_conf = settings['google_drive']

    TRANSMISSION_USER = trans_conf['TRANSMISSION_USER']
    TRANSMISSION_PASSWD = trans_conf['TRANSMISSION_PASSWD']
    TRANSMISSION_DOWNLOAD_PATH = trans_conf['TRANSMISSION_DOWNLOAD_PATH']

    CREDENTIAL_INIT = drive_conf['CREDENTIAL_INIT']
    CREDENTIAL_RETRIVE = drive_conf['CREDENTIAL_RETRIVE']
    ROOT_NAME = drive_conf['ROOT_NAME']
    DRIVE_DOWNLOAD_PATH = drive_conf['DRIVE_DOWNLOAD_PATH']

    '''start'''
    trans = Transmission(TRANSMISSION_USER, TRANSMISSION_PASSWD)
    drive = Drive(CREDENTIAL_INIT,CREDENTIAL_RETRIVE)

    root_id = drive.get_list(file=False, name=ROOT_NAME)[0]['id']

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