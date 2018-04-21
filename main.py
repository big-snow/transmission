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
    args = util.sys_args()
    conf = util.fromJson(open(args[1]))
    
    drive = Drive(args[2], args[3])
    transmission = Transmission(conf['transmission-user'], conf['transmission-passwd'])

    for folder in conf['download']:
        root_name = folder['drive-root']
        root_id = drive.get_list(file=False, name=root_name)[0]['id']    
        
        download(transmission, drive, root_id, '/data')