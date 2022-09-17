import json
import os
import subprocess

from typing import List

from volume import Volume, TVolumeCreate, TVolumeMount

def _parse_size_str(size: str) -> (str, int):
    ''' 
    '1M' -> (1, 'M')
    '''
    return (int(size[:-1]), size[-1])

class VolumeManager:
    @staticmethod
    def create_sparse_file(path: str, size: int, unit: str) -> None:
        '''Create a sparse file, see https://www.wefearchange.org/2017/01/sparsefiles.rst.html
        '''
        os.system(f"truncate -s{size}{unit} {path}")
  

    @staticmethod
    def create_loop_device(loopfile: str):
        os.system(f"sudo losetup -fP {loopfile}")

    @staticmethod
    def list_loop_devices(filter: str = '') -> List[str]:
        '''
        Args:
            filter: str - Filter by name of loop device's backing file
        '''
        return  [loop_device for loop_device in 
        json.loads(subprocess.check_output(['losetup', '-J']))['loopdevices'] if filter in loop_device['back-file'] ]

    @staticmethod
    def mkfs_btrfs(device: str):
        os.system(f"sudo mkfs.btrfs {device}")

    @staticmethod
    def create_volume(volume_create: TVolumeCreate):
        VolumeManager.create_sparse_file(volume_create.name, *_parse_size_str(volume_create.size))
        VolumeManager.create_loop_device(volume_create.name)
        loopback_device: str = VolumeManager.list_loop_devices(volume_create.name)[0]['name']
        VolumeManager.mkfs_btrfs(loopback_device)
        return Volume()

    @staticmethod
    def mount_volume(volume_mount: TVolumeMount):
        os.system(f"sudo mount {volume_mount.name} {volume_mount.mount_point}")