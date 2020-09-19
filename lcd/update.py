import requests
import json
import os
import subprocess

class UpdateError(Exception):
    pass

class Update:
    def _run(self, command='ls -lah'):
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode().strip()

    def get_passive_partition(self):
        cmdline = self._run('cat /proc/cmdline')
        p2 = '/dev/mmcblk0p2'
        p3 = '/dev/mmcblk0p3'
        
        if p2 in cmdline:
            return p3
        elif p3 in cmdline:
            return p2
        else:
            raise UpdateError('Passive partition not found')

    def download(self, 
                url='https://github.com/wipfli/buildroot/releases/download/v0.1.0/rootfs.ext2.xz', 
                passive_partition='/dev/mmcblk0p3',
                progress_callback=lambda percentage: (), 
                total_size=1):
        
        r = requests.get(url, stream=True, timeout=10)
        
        r.raise_for_status()
        chunk_i = 0
        last_percentage = 0
        progress_callback(last_percentage)
        
        xz_command = ['xz', '-d']
        xz_pipe = subprocess.Popen(xz_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        
        dd_command = ['dd', 'of=' + passive_partition, 'bs=1M']
        dd_pipe = subprocess.Popen(dd_command, stdin=xz_pipe.stdout)
        
        chunk_size = 8192
        for chunk in r.iter_content(chunk_size): 
            xz_pipe.stdin.write(chunk)
            chunk_i += 1
            percentage = min(int(100 * chunk_i * chunk_size / total_size), 100)
            if percentage > last_percentage:
                last_percentage = percentage
                progress_callback(percentage)
        
        xz_pipe.stdin.close()
        xz_pipe.wait()        
        dd_pipe.wait()
            
    def get_checksum_rootfs(self, passive_partition='/dev/mmcblk0p3'):
        result = ''
        self._run('mount ' + passive_partition + ' /passive')
        tar_pipe = subprocess.Popen(['tar', 'c', '/passive'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = subprocess.check_output('sha3sum', stdin=tar_pipe.stdout).decode().split(' ')[0]
        self._run('umount /passive')
        return result

    def get_checksum_boot(self, passive_partition='/dev/mmcblk0p3'):
        result = ''
        self._run('mount -t vfat /dev/mmcblk0p1 /boot')

        folder = '/boot/os-p2'
        if passive_partition == '/dev/mmcblk0p3':
            folder = '/boot/os-p3'

        tar_pipe = subprocess.Popen(['tar', 'c', '.', '-C', folder], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = subprocess.check_output('sha3sum', stdin=tar_pipe.stdout).decode().split(' ')[0]
        self._run('umount /boot')
        return result

    def flash_boot_select(self, passive_partition='/dev/mmcblk0p3'):
        self._run('mount -t vfat /dev/mmcblk0p1 /boot')
        
        if passive_partition == '/dev/mmcblk0p2':
            self._run('echo "cmdline=cmdline-p2.txt" > /boot/select.txt')
        elif passive_partition == '/dev/mmcblk0p3':
            self._run('echo "cmdline=cmdline-p3.txt" > /boot/select.txt')
        else:
            raise UpdateError('Passive partition not matched')
        
        self._run('umount /boot')
        