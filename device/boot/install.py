import shutil

shutil.copyfile('/boot/config.txt', '/boot/config.txt.backup')
shutil.copyfile('/boot/cmdline.txt', '/boot/cmdline.txt.backup')
shutil.copyfile('/etc/modules', '/etc/modules.backup')

boot_config_content = '''
dtparam=i2c_arm=on
dtoverlay=i2c-gpio,bus=3
disable_splash=1
dtoverlay=pi3-disable-bt
dtoverlay=sdtweak,overclock_50=100
boot_delay=0
force_turbo=1
'''

with open('/boot/config.txt', 'w') as f:
    f.write(boot_config_content)

boot_cmdline_content = ''
with open('/boot/cmdline.txt', 'r') as f:
    boot_cmdline_content = f.readline()

boot_cmdline_content = boot_cmdline_content.strip()

if 'quiet' not in boot_cmdline_content:
    boot_cmdline_content += ' quiet\n'

    with open('/boot/cmdline.txt', 'w') as f:
        f.write(boot_cmdline_content)


etc_modules_content = ''
with open('/etc/modules') as f:
    etc_modules_content = ''.join(f.readlines())

if 'i2c-dev' not in etc_modules_content:
    etc_modules_content += '\ni2c-dev\n'
    with open('/etc/modules', 'w') as f:
        f.write(etc_modules_content)

