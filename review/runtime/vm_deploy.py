from vm_apps import *
def deployment():
 t('24 unused names',['24-01'],'''! getent passwd labapp
! getent group labapp
test ! -e /opt/labapp
test ! -e /var/lib/labapp
test ! -e /etc/systemd/system/labapp.service
''',user='root')
 if not t('24 service identity and directories',['24-02','24-03'],B('24-02','24-03'),user='root'):return
 if not t('24 install release v1',['24-04'],B('24-04'),user='root'):return
 put(LAB/'deploy/labapp.service',(BASE/'examples/labapp.service').read_text().replace('ExecStart=/usr/bin/java','ExecStart='+JDK+'/bin/java'))
 p=start('exec '+JDK+'/bin/java -jar /opt/labapp/current/app.jar',user='labapp')
 try:
  record('24 foreground service identity',ready(),'Foreground-equivalent managed subprocess as labapp; stopped before systemd')
 finally:stop(p)
 if not t('24 install verify enable start',['24-06','24-07','24-08','24-10'],B('24-10'),user='root',note='Unit pins verified JDK21 absolute path; file editing automated'):return
 t('24 service evidence',['24-11'],B('24-11')+'''
pid=$(systemctl show -p MainPID --value labapp)
test "$(ps -p "$pid" -o user= | xargs)" = labapp
test "$(getenforce)" = Enforcing
systemctl show labapp -p NoNewPrivileges -p ProtectHome -p ProtectSystem -p PrivateTmp
sudo -u labapp test ! -w /opt/labapp/current/app.jar
sudo -u labapp test -w /var/lib/labapp
''',user='root')
 # Rebuild v2 while v1 remains installed and running.
 put(LAB/'java-app/LabServer.java',(BASE/'examples/java-app/LabServer.java').read_text().replace('String version = "v1"','String version = "v2"'))
 t('24 compile v2',['24-12'],J+'''cd ~/linux-lab/java-app
javac --release 21 -d classes LabServer.java
jar --create --file app.jar --main-class LabServer -C classes .
''')
 t('24 install v2',['24-12'],B('24-12'),user='root')
 t('24 switch v2',['24-13'],B('24-13')+'\ntest "$(curl -fsS http://127.0.0.1:8080/)" = "Hola Euler v2"',user='root')
 t('24 rollback v1',['24-14'],B('24-14')+'\ntest "$(curl -fsS http://127.0.0.1:8080/)" = "Hola Euler v1"',user='root')
 # Prove the guard stops before the running service is changed.
 t('24 dangling next link guard',[],'''pid=$(systemctl show -p MainPID --value labapp)
ln -sT missing-target /opt/labapp/current.next
trap 'test ! -L /opt/labapp/current.next || unlink /opt/labapp/current.next' EXIT
if ('''+B('24-13')+'''); then exit 1; fi
test "$(systemctl show -p MainPID --value labapp)" = "$pid"
test "$(curl -fsS http://127.0.0.1:8080/)" = 'Hola Euler v1'
''',user='root')
 t('24 fault diagnosis and recovery',[],'''test ! -e /opt/labapp/releases/broken
install -d -m 0755 /opt/labapp/releases/broken
systemctl stop labapp
ln -sT releases/broken /opt/labapp/current.next
mv -Tf /opt/labapp/current.next /opt/labapp/current
systemctl start labapp
sleep 2
systemctl stop labapp
journalctl -u labapp -n 30 --no-pager | grep -F 'Unable to access jarfile'
'''+B('24-14'),user='root',note='Broken release only in test service; journal evidence captured and v1 restored')
 t('23 security and journal',['23-01'],B('23-01')+'\njournalctl -u labapp -b -n 20 --no-pager',user='root')
if __name__=='__main__':deployment()
