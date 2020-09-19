import update

def test_run():
    u = update.Update()
    u._run('ls -lah /root')
    
def test_get_current_release():
    u = update.Update()
    assert u.get_current_release() == 'v1.0.0'
    
def test_get_releases():
    u = update.Update()
    assert 'v1.0.0' in u.get_releases()
    
def test_get_passive_partition():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    assert u._get_passive_partition() == '/dev/mmcblk0p3'
    
def test_get_total_size():
    u = update.Update()
    assert u._get_total_size(release='v1.0.0') == 55260960.0
    
def test_download_checksums():
    u = update.Update()
    checksums = u._download_checksums(release='v1.0.0')
    assert 'rootfs' in checksums
    assert 'boot' in checksums
    
def test_download_rootfs():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    u._download_rootfs(release='v1.0.0', 
                       passive_partition='/dev/mmcblk0p3',
                       progress_callback=lambda percentage: print(percentage), 
                       total_size=55260960.0)
    
def test_download_boot():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    u._download_boot(release='v1.0.0',
                     passive_partition='/dev/mmcblk0p3')
    
def test_get_checksum_rootfs():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    checksum = u._get_checksum_rootfs(passive_partition='/dev/mmcblk0p3')
    assert checksum == '...'
    
def test_get_checksum_boot():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    checksum = u._get_checksum_boot(passive_partition='/dev/mmcblk0p3')
    assert checksum == '...'
    
def test_flash_boot_select():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    u._flash_boot_select(passive_partition='/dev/mmcblk0p3')
    
def test_install():
    '''
    This test assumes that the active partition is /dev/mmcblk0p2.
    '''
    u = update.Update()
    u.install(release='v1.0.0',
              update_callback=lambda text: print(text))
    
if __name__ == '__main__':
    test_run()
    test_get_current_release()
    test_get_releases()
    test_get_passive_partition()
    test_get_total_size()
    test_download_checksums()
    test_download_rootfs()
    test_download_boot()
    test_get_checksum_rootfs()
    test_get_checksum_boot()
    test_flash_boot_select()
    test_install()