import requests
import json
import subprocess
import time


request_timeout = 30


class UpdateError(Exception):
    pass


def get_current_release():
    try:
        with open('/root/release.json') as f:
            return json.load(f)
    except FileNotFoundError:
        raise UpdateError('FileNotFoundError')
    except json.JSONDecodeError:
        raise UpdateError('JSONDecodeError')


def get_releases():
    result = []

    url = 'https://api.github.com/repos/wipfli/buildroot/releases'
    try:
        r = requests.get(url, timeout=request_timeout)
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')
    if r.status_code != 200:
        raise UpdateError('Non 200 status code')

    try:
        releases = json.loads(r.text)
    except json.JSONDecodeError:
        raise UpdateError('JSONDecodeError')

    for release in releases:
        if 'tag_name' not in release:
            raise UpdateError('tag_name not in releases')
        result.append(release['tag_name'])

    return result


def install(release='v1.0.0', update_callback=lambda text: ()):
    passive_partition = _get_passive_partition()
    total_size = _get_total_size(release)

    def progress_callback(percentage):
        text = 'ROOTFS ' + str(percentage) + ' %'
        update_callback(text)

    _download_rootfs(release=release,
                     passive_partition=passive_partition,
                     progress_callback=progress_callback,
                     total_size=total_size)

    update_callback('DOWNLOAD BOOT')

    _download_boot(release=release, passive_partition=passive_partition)

    update_callback('MAKE CHECKSUMS')
    checksums = _download_checksums(release=release)
    checksum_rootfs = _get_checksum_rootfs(passive_partition)
    checksum_boot = _get_checksum_boot(passive_partition=passive_partition)

    if 'rootfs' not in checksums:
        raise UpdateError('Checksum file misses rootfs')

    if 'boot' not in checksums:
        raise UpdateError('Checksum file misses boot')

    if checksums['rootfs'] != checksum_rootfs:
        raise UpdateError('Checksum rootfs is wrong')

    if checksums['boot'] != checksum_boot:
        raise UpdateError('Checksum boot is wrong')

    update_callback('CHECKSUMS OK')

    time.sleep(1)

    _flash_boot_select(passive_partition=passive_partition)


def create_checksums_json():
    passive_partition = _get_passive_partition()
    checksum_rootfs = _get_checksum_rootfs(passive_partition=passive_partition)
    checksum_boot = _get_checksum_boot(passive_partition=passive_partition)
    return json.dumps({'rootfs': checksum_rootfs, 'boot': checksum_boot})


def _run(command='ls -lah'):
    try:
        return subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT).decode().strip()
    except subprocess.CalledProcessError:
        raise UpdateError('CalledProcessError')


def _get_passive_partition():
    cmdline = _run('cat /proc/cmdline')
    p2 = '/dev/mmcblk0p2'
    p3 = '/dev/mmcblk0p3'

    if p2 in cmdline:
        return p3
    elif p3 in cmdline:
        return p2
    else:
        raise UpdateError('Passive partition not found')


def _get_total_size(release='v1.0.0'):
    url = 'https://github.com/wipfli/buildroot/releases/download/' + \
        release + '/rootfs.ext2.xz'
    try:
        r = requests.get(url, stream=True, timeout=request_timeout)
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')

    try:
        return float(r.headers['Content-Length'])
    except KeyError:
        raise UpdateError('Content-Length not in headers')


def _download_checksums(release='v1.0.0'):
    url = 'https://github.com/wipfli/buildroot/releases/download/' + \
        release + '/checksums.json'
    try:
        r = requests.get(url, timeout=request_timeout)
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')
    if r.status_code != 200:
        raise UpdateError('Non 200 status code')

    try:
        return json.loads(r.text)
    except json.JSONDecodeError:
        raise UpdateError('JSONDecodeError')


def _download_rootfs(
        release='v1.0.0',
        passive_partition='/dev/mmcblk0p3',
        progress_callback=lambda percentage: (),
        total_size=1.0):
    try:
        url = 'https://github.com/wipfli/buildroot/releases/download/' + \
            release + '/rootfs.ext2.xz'
        r = requests.get(url, stream=True, timeout=request_timeout)

        r.raise_for_status()
        chunk_i = 0
        last_percentage = 0
        progress_callback(last_percentage)

        xz_command = ['xz', '-d']
        xz_pipe = subprocess.Popen(
            xz_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

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
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')


def _download_boot(release='v1.0.0', passive_partition='/dev/mmcblk0p3'):
    _run('mount -t vfat /dev/mmcblk0p1 /boot')
    folder = '/boot/os-p2'
    if passive_partition == '/dev/mmcblk0p3':
        folder = '/boot/os-p3'

    _run('rm -rf ' + folder)
    _run('mkdir ' + folder)

    try:
        url = 'https://github.com/wipfli/buildroot/releases/download/' + \
            release + '/boot.tar.xz'
        r = requests.get(url, stream=True, timeout=request_timeout)

        r.raise_for_status()

        xz_command = ['xz', '-d']
        xz_pipe = subprocess.Popen(
            xz_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        tar_command = ['tar', 'x', '-C', folder]
        tar_pipe = subprocess.Popen(tar_command, stdin=xz_pipe.stdout)

        chunk_size = 8192
        for chunk in r.iter_content(chunk_size):
            xz_pipe.stdin.write(chunk)

        xz_pipe.stdin.close()
        xz_pipe.wait()
        tar_pipe.wait()
    except requests.exceptions.Timeout:
        raise UpdateError('Timout')
    except requests.exceptions.ConnectionError:
        raise UpdateError('ConnectionError')

    _run('umount /boot')


def _get_checksum_rootfs(passive_partition='/dev/mmcblk0p3'):
    result = ''
    _run('mount -o ro ' + passive_partition + ' /passive')
    tar_pipe = subprocess.Popen(
        ['tar', 'c', '/passive'], stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    result = subprocess.check_output(
        'sha3sum', stdin=tar_pipe.stdout).decode().split(' ')[0]
    _run('umount /passive')
    return result


def _get_checksum_boot(passive_partition='/dev/mmcblk0p3'):
    result = ''
    _run('mount -t vfat /dev/mmcblk0p1 /boot')

    folder = '/boot/os-p2'
    if passive_partition == '/dev/mmcblk0p3':
        folder = '/boot/os-p3'

    find_pipe = subprocess.Popen(
        ['find', '.', '-exec', 'sha3sum', '{}', '\\;'],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=folder)
    result = subprocess.check_output(
        'sha3sum', stdin=find_pipe.stdout).decode().split(' ')[0]
    _run('umount /boot')
    return result


def _flash_boot_select(passive_partition='/dev/mmcblk0p3'):
    _run('mount -t vfat /dev/mmcblk0p1 /boot')

    if passive_partition == '/dev/mmcblk0p2':
        _run('echo "cmdline=cmdline-p2.txt\r\n' +
             'os_prefix=os-p2/" > /boot/select.txt')
    elif passive_partition == '/dev/mmcblk0p3':
        _run('echo "cmdline=cmdline-p3.txt\r\n' +
             'os_prefix=os-p3/" > /boot/select.txt')
    else:
        raise UpdateError('Passive partition not matched')

    _run('umount /boot')
