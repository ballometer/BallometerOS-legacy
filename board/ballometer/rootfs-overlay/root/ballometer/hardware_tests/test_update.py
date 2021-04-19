from ballometer import update as u


def test_run():
    u._run('ls -lah /root')


def test_get_current_release():
    u.get_current_release()


def test_get_releases():
    assert 'v1.0.0' in u.get_releases()


def test_get_passive_partition():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    assert u._get_passive_partition() == '/dev/mmcblk0p3'


def test_get_total_size():
    assert u._get_total_size(release='v1.0.0') == 55260960.0


def test_download_checksums():
    checksums = u._download_checksums(release='v1.0.0')
    assert 'rootfs' in checksums
    assert 'boot' in checksums


def test_download_rootfs():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u._download_rootfs(release='v1.0.0',
                       passive_partition='/dev/mmcblk0p3',
                       progress_callback=lambda percentage: print(percentage),
                       total_size=55260960.0)


def test_download_boot():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u._download_boot(release='v1.0.0',
                     passive_partition='/dev/mmcblk0p3')


def test_get_checksum_rootfs():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    checksum = u._get_checksum_rootfs(passive_partition='/dev/mmcblk0p3')
    reference = '9b987e4275346ca30de0ae331b3eabbf50282298411fa427dc2f8ba0'
    assert checksum == reference


def test_get_checksum_boot():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    checksum = u._get_checksum_boot(passive_partition='/dev/mmcblk0p3')
    reference = '19f7cc8c95438d774bb86ca2e0c0442eb48efa047881def43bc3009f'
    assert checksum == reference


def test_flash_boot_select():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u._flash_boot_select(passive_partition='/dev/mmcblk0p3')


def test_install():
    print('''
    This test assumes that the active partition is /dev/mmcblk0p2.
    ''')
    u.install(release='v1.0.0',
              update_callback=lambda text: print(text))


def test_create_checksums_json():
    assert 'rootfs' in u.create_checksums_json()


def test_all():
    print('test_run()')
    test_run()
    print('test_get_current_release()')
    test_get_current_release()
    print('test_get_releases()')
    test_get_releases()
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
    test_get_checksum_rootfs()
    print('test_get_checksum_boot()')
    test_get_checksum_boot()
    print('test_flash_boot_select()')
    test_flash_boot_select()
    print('test_install()')
    test_install()
    print('test_create_checksums_json()')
    test_create_checksums_json()


if __name__ == '__main__':
    test_all()
