from ballometer import update as u


def test_run():
    u._run('ls -lah /root')


def test_get_installed_release():
    u.get_installed_release()


def test_get_available_releases():
    assert 'v2.0.0-rc.1' in u.get_available_releases()


def test_get_passive_partition():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    assert u._get_passive_partition() == '/dev/mmcblk0p3'


def test_get_total_size():
    assert u._get_total_size(release='v2.0.0-rc.1') == 41294496.0


def test_download_checksums():
    checksums = u._download_checksums(release='v2.0.0-rc.1')
    assert 'rootfs.ext2.xz' in checksums
    assert 'boot.tar.xz' in checksums


def test_download_rootfs():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u._download_rootfs(release='v2.0.0-rc.1',
                       passive_partition='/dev/mmcblk0p3',
                       progress_callback=lambda percentage: print(percentage),
                       total_size=41294496.0)


def test_download_boot():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u._download_boot(release='v2.0.0-rc.1',
                     passive_partition='/dev/mmcblk0p3')


def test_flash_boot_select():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u._flash_boot_select(passive_partition='/dev/mmcblk0p3')
    # undo /boot/select.txt update:
    u._flash_boot_select(passive_partition='/dev/mmcblk0p2')


def test_install():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u.install(release='v2.0.0-rc.1',
              update_callback=lambda text: print(text))
    # undo /boot/select.txt update:
    u._flash_boot_select(passive_partition='/dev/mmcblk0p2')


def test_all():
    print('test_run()')
    test_run()
    print('test_get_installed_release()')
    test_get_installed_release()
    print('test_get_available_releases()')
    test_get_available_releases()
    print('test_get_passive_partition()')
    test_get_passive_partition()
    print('test_get_total_size()')
    test_get_total_size()
    print('test_download_checksums()')
    test_download_checksums()
    print('test_download_rootfs()')
    test_download_rootfs()
    print('test_download_boot()')
    test_download_boot()
    print('test_get_checksum_rootfs()')
    test_flash_boot_select()
    print('test_install()')
    test_install()


if __name__ == '__main__':
    test_all()
