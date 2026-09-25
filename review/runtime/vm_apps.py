from vm_runtime import *
import urllib.request,urllib.error,pty,select,fcntl,termios,struct
JDK='/usr/lib/jvm/java-21-openjdk'
J='export JAVA_HOME='+JDK+'; export PATH="$JAVA_HOME/bin:$PATH"; '
def start(code,user='eulercheck'):
 log=open(BASE/'applications.log','a')
 p=subprocess.Popen(['runuser','-u',user,'--','env','HOME='+str(HOME),'LC_ALL=C','PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin','bash','-c',code],cwd=HOME if user=='eulercheck' else '/tmp',stdout=log,stderr=log,start_new_session=True)
 p._log=log;return p
def stop(p):
 if p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=15)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
 p._log.close()
def ready(body='ok\n'):
 for _ in range(60):
  try:
   with urllib.request.urlopen('http://127.0.0.1:8080/health',timeout=1) as r:
    if r.read().decode()==body:return True
  except Exception:pass
  time.sleep(.2)
 return False
def record(name,passed,note=''):
 results.append({'name':name,'blocks':[],'identity':'eulercheck','passed':passed,'adaptation':note})
 RESULT.write_text(json.dumps(results,indent=2)+'\n')
 print(('PASS ' if passed else 'FAIL ')+name,flush=True)
def keys(command,events):
 master,slave=pty.openpty();fcntl.ioctl(slave,termios.TIOCSWINSZ,struct.pack('HHHH',24,100,0,0))
 p=subprocess.Popen(['runuser','-u','eulercheck','--','env','HOME='+str(HOME),'TERM=xterm','LC_ALL=C','bash','-c',command],stdin=slave,stdout=slave,stderr=slave,start_new_session=True)
 os.close(slave);out=bytearray()
 def pump(seconds):
  end=time.monotonic()+seconds
  while time.monotonic()<end:
   if select.select([master],[],[],.05)[0]:
    try:out.extend(os.read(master,65536))
    except OSError:break
 for delay,data in events:
  pump(delay);os.write(master,data)
 pump(.5)
 try:rc=p.wait(timeout=4)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGTERM);rc=p.wait()
 os.close(master)
 return rc,bytes(out)
def recovery():
 t('02 man after coreutils-help install',['02-03'],'help cd; ls --help; MANPAGER=cat man ls')
 t('12 normal-login PATH',['12-01','12-02','12-03'],B('12-01','12-02','12-03'),note='PATH matches verified runuser -l login environment',timeout=60)
 rc,out=keys('less "$HOME/linux-lab/text/app.log"',[(.4,b'/ERROR\n'),(.2,b'q')])
 record('05 interactive less search quit',rc==0 and b'ERROR' in out)
 rc,out=keys('man ls',[(.5,b'q')])
 record('02 interactive man quit',rc==0 and b'LS' in out)
 put(LAB/'editor/placeholder','')
 rc,out=keys('vim -Nu NONE -n "$HOME/linux-lab/editor/note.txt"',[(.4,b'iLinux lab\nsecond lab\nthird line\x1b'),(.2,b'ggdd'),(.2,b'u'),(.2,b'\x12'),(.2,b'u'),(.2,b'yyp'),(.2,b'/Linux\n'),(.2,b':set number\n'),(.2,b':%s/lab/practice/gc\n'),(.2,b'a'),(.2,b':wq\n')])
 expected='Linux practice\nLinux practice\nsecond practice\nthird line\n'
 record('06 Vim insert delete undo redo copy search confirm substitute save',rc==0 and (LAB/'editor/note.txt').read_text()==expected)
 rc,out=keys('vim -Nu NONE -n "$HOME/linux-lab/editor/note.txt"',[(.3,b'ggidiscard\x1b'),(.2,b':q!\n')])
 record('06 Vim discard unsaved changes',rc==0 and (LAB/'editor/note.txt').read_text()==expected)
def java():
 put(LAB/'java-app/LabServer.java',(BASE/'examples/java-app/LabServer.java').read_text())
 t('22 baseline default JDK mismatch',['22-05'],'cd ~/linux-lab/java-app; mkdir -p classes; javac --release 21 -d classes LabServer.java',expected=2,note='Reproduces uncorrected Java 8 default; manuscript correction selects JDK 21 explicitly')
 t('22 selected JDK toolchain',['22-01','22-02'],J+'java -version; javac -version; mvn -version; command -v java; command -v javac; command -v jar')
 ok=t('22 compile JDK21 and package',['22-03','22-04','22-05'],J+'''cd ~/linux-lab/java-app
mkdir -p classes
javac --release 21 -d classes LabServer.java
jar --create --file app.jar --main-class LabServer -C classes .
sha256sum app.jar
''')
 if not ok:return
 p=start(J+'exec java -jar ~/linux-lab/java-app/app.jar')
 try:
  assert ready(),'Java service did not become ready'
  t('22 HTTP responses and loopback binding',['22-06'],B('22-06')+'''
test "$(curl -fsS http://127.0.0.1:8080/)" = 'Hola Euler v1'
test "$(curl -fsS http://127.0.0.1:8080/health)" = ok
test "$(curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/missing)" = 404
test "$(curl -sS -X POST -D "$HOME/post.headers" -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/)" = 405
grep -i '^Allow: GET' "$HOME/post.headers"
test "$(curl -sSI -o "$HOME/head.headers" -w '%{http_code}' http://127.0.0.1:8080/)" = 405
ss -ltnH 'sport = :8080' | grep -E '127\.0\.0\.1\]?:8080'
''')
  t('20 health success; 24 readiness branches',['20-04','24-09'],'''bash ~/linux-lab/scripts/check-health.sh
bash ~/linux-lab/scripts/wait-ready.sh v1
if bash ~/linux-lab/scripts/wait-ready.sh v2; then exit 1; else test "$?" -eq 1; fi
if bash ~/linux-lab/scripts/wait-ready.sh; then exit 1; else test "$?" -eq 2; fi
''')
 finally:stop(p)
 t('22 shutdown releases port',[],"! ss -ltnH 'sport = :8080' | grep -q .")
def spring():
 for file in (BASE/'examples/spring-lab').rglob('*'):
  if file.is_file():put(LAB/'spring-lab'/file.relative_to(BASE/'examples/spring-lab'),file.read_text())
 t('22 Maven version',['22-11'],J+'mvn -version')
 settings=os.environ.get('HOLA_MAVEN_SETTINGS','')
 opts=' -s '+settings if settings else ''
 ok=t('22 Spring package'+(' with mirror' if settings else ''),['22-07','22-08','22-09','22-10','22-11'],J+'cd ~/linux-lab/spring-lab; mvn -U -B -ntp'+opts+' package',timeout=540,note='Exact project version; explicit isolated mirror settings when selected')
 if not ok:return
 p=start(J+'exec java -jar ~/linux-lab/spring-lab/target/spring-lab-1.0.0.jar')
 try:
  assert ready(),'Spring did not become ready'
  t('22 Spring endpoints and binding',['22-11'],'''test "$(curl -fsS http://127.0.0.1:8080/health)" = ok
test "$(curl -fsS http://127.0.0.1:8080/)" = 'Hola Euler Spring'
ss -ltnH 'sport = :8080' | grep -E '127\.0\.0\.1\]?:8080'
''')
 finally:stop(p)
 t('22 Spring stopped',[],"! ss -ltnH 'sport = :8080' | grep -q .")
if __name__=='__main__':
 import sys
 for phase in sys.argv[1:]:globals()[phase]()
