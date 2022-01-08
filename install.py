import os
import subprocess

if os.getuid() != 0:
    print('You must be root to install.  Exiting...')
    exit()


if 'usage: git' not in subprocess.getoutput('/bin/git'):
    print('git is not installed.  Exiting...')
    exit()

bin_path = '/opt/postfix-filter-loop'
os.mkdir(bin_path)
os.system(f'adduser --home {bin_path} postfixfilterloop')

os.system(f'/bin/git -C /opt/ clone https://github.com/9cb14c1ec0/postfix-filter-loop')
os.system('chown -hR postfixfilterloop /opt/postfix-filter-loop')
os.system(f'cp {os.path.join(bin_path, "postfix-filter-loop.service")} /etc/systemd/system/postfix-filter-loop.service')
os.system('systemctl daemon-reload')
os.system('systemctl enable --now postfix-filter-loop.timer')
