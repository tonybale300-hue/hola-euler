from vm_runtime import *
def ssh_cases():
 t('13 generate client keys',['13-03'],'''mkdir -p ~/.ssh; chmod 700 ~/.ssh
test ! -e ~/.ssh/linux-lab_ed25519
ssh-keygen -q -t ed25519 -N '' -f ~/.ssh/linux-lab_ed25519
ssh-keygen -q -t ed25519 -N '' -f ~/.ssh/copy-test
''',note='Empty key passphrase for isolated automated fixture; no existing key overwritten')
 first=(HOME/'.ssh/linux-lab_ed25519.pub').read_text()
 host=Path('/etc/ssh/ssh_host_ed25519_key.pub').read_text().strip()
 put(HOME/'.ssh/authorized_keys',first)
 put(HOME/'.ssh/known_hosts','localhost '+host+'\n')
 os.chmod(HOME/'.ssh/authorized_keys',0o600)
 t('13 label test SSH directory',[], 'restorecon -R /home/eulercheck/.ssh',user='root')
 opts='-o BatchMode=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/home/eulercheck/.ssh/known_hosts'
 t('13 public key login',['13-01','13-04'],'test "$(ssh '+opts+' -p 22 -i ~/.ssh/linux-lab_ed25519 eulercheck@localhost id -un)" = eulercheck',note='Actual test endpoint localhost:22 and test username replace illustrative NAT endpoint')
 t('13 ssh-copy-id adds second key',['13-04'],'ssh-copy-id -i ~/.ssh/copy-test.pub -p 22 -o IdentityFile=/home/eulercheck/.ssh/linux-lab_ed25519 '+opts+' eulercheck@localhost\n'+'test "$(ssh '+opts+' -p 22 -i ~/.ssh/copy-test eulercheck@localhost id -un)" = eulercheck',note='First fixture key bootstraps login; ssh-copy-id genuinely installs a second test key')
 t('13 SCP transfer checksum',['13-05'],'scp '+opts+' -P 22 -i ~/.ssh/copy-test ~/linux-lab/java-app/app.jar eulercheck@localhost:uploaded-app.jar\ncmp ~/linux-lab/java-app/app.jar ~/uploaded-app.jar',note='Only transfers test JAR within the isolated user account')
if __name__=='__main__':ssh_cases()
