import shutil

shutil.move('/boot/config.txt.backup', '/boot/config.txt')
shutil.move('/boot/cmdline.txt.backup', '/boot/cmdline.txt')