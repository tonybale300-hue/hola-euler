from pathlib import Path
import argparse,json,os,pwd,subprocess,time,signal
BASE=Path('/var/tmp/hola-euler-test-20260924');HOME=Path('/home/eulercheck');LAB=HOME/'linux-lab'
BLOCKS=json.loads((BASE/'blocks.json').read_text())
RESULT=BASE/'runtime-results.json'
results=json.loads(RESULT.read_text()) if RESULT.exists() else []
def B(*ids):return '\n'.join(BLOCKS[i]['code'] for i in ids)
def put(path,content):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
 u=pwd.getpwnam('eulercheck');os.chown(path,u.pw_uid,u.pw_gid)
 parent=path.parent
 while parent!=HOME and HOME in parent.parents:os.chown(parent,u.pw_uid,u.pw_gid);parent=parent.parent
def t(name,ids,code,user='eulercheck',cwd=HOME,expected=0,timeout=90,note=''):
 cmd=['env','HOME='+str(HOME),'USER='+user,'LOGNAME='+user,'LC_ALL=C','PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin','bash','--noprofile','--norc','-e','-o','pipefail','-c',code]
 if user!='root':cmd=['runuser','-u',user,'--',*cmd]
 started=time.monotonic()
 try:r=subprocess.run(cmd,cwd=cwd,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=timeout);rc=r.returncode;out=r.stdout;err=r.stderr
 except subprocess.TimeoutExpired as e:rc=124;out=str(e.stdout or '');err='TIMEOUT '+str(e.stderr or '')
 row={'name':name,'blocks':ids,'identity':user,'exit':rc,'expected_exit':expected,'passed':rc==expected,'seconds':round(time.monotonic()-started,2),'adaptation':note,'stdout':out[-10000:],'stderr':err[-4000:]}
 results.append(row);RESULT.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 print(('PASS ' if row['passed'] else 'FAIL ')+name,flush=True)
 return row['passed']
def foundation():
 t('00 workspace',['00-01'],B('00-01')+'\ntest "$PWD" = /home/eulercheck/linux-lab')
 t('01 platform',['01-01'],B('01-01')+'\ntest "$(uname -m)" = x86_64; grep -q LTS-SP4 /etc/os-release')
 t('02 shell and help',['02-01','02-02','02-03'],B('02-01','02-02','02-03').replace('man ls','MANPAGER=cat man ls'),note='Noninteractive man pager; keyboard pager tested separately')
 t('02 intentional typo',['02-04'],B('02-04'),expected=127)
 t('03 paths',['03-01','03-02','03-04'],B('03-01','03-02','03-04')+'\ntest "$PWD" = "$HOME/linux-lab/paths/reading notes"')
 t('03 failed cd retains directory',['03-03'],'cd ~/linux-lab/paths; before=$PWD; if cd missing; then exit 1; fi; test "$PWD" = "$before"; pwd',note='Expected failure asserted')
 t('03 exercise directories',[],'mkdir -p ~/linux-lab/project/src ~/linux-lab/project/docs; cd ~/linux-lab/project/src; cd ../docs; test "$PWD" = "$HOME/linux-lab/project/docs"')
 t('04 files and links',['04-01','04-02','04-03','04-04','04-05','04-06'],B('04-01','04-02','04-03','04-04','04-05','04-06').replace('rm -i hello.txt',"printf 'y\\n' | rm -i hello.txt")+'''
test ! -e hello.txt; test -f archive/draft.txt; test -f archive-copy/draft.txt
test "$(stat -c %i original.txt)" = "$(stat -c %i hard.txt)"
test "$(readlink soft.txt)" = original.txt
cp original.txt original.bak; mv original.bak archive/; cmp original.txt archive/original.bak
printf '%s\n' changed > hard.txt; test "$(cat original.txt)" = changed
rm original.txt; test -f hard.txt; test -L soft.txt; test ! -e soft.txt
printf '%s\n' changed > original.txt
mkdir empty; rmdir empty
''',note='rm -i supplied y; link deletion affects only created files')
 t('05 text',['05-01','05-03','05-04','05-05','05-06'],B('05-01','05-03','05-04','05-05','05-06')+'''
test "$(wc -l < app.log)" -eq 6
test "$(head -n 1 sorted.txt)" = apple
test "$(uniq -c sorted.txt | awk '{s+=$1} END{print s}')" -eq 4
test "$(cut -d : -f1 roles.txt | head -n1)" = alex
printf '%s\n' pear apple pear apple banana pear > exercise-list.txt
sort exercise-list.txt > exercise-sorted.txt
test "$(uniq -c exercise-sorted.txt | awk '{s+=$1} END{print s}')" -eq 6
''')
 t('05 pager content',['05-02'],'less -F -X app.log',cwd=LAB/'text',note='Keyboard interaction separately tested')
 t('07 identity',['07-01','07-02'],B('07-01','07-02')+'\ntest "$(id -u)" -ne 0')
 t('07 sudo denial',['07-03'],'sudo -n -l',expected=1,note='Ordinary test user has no sudo grant; authorized root runs administrator steps')
 t('07 account and group',['07-04','07-05'],'''! getent passwd labreader
sudo useradd -m labreader
id labreader
! getent group labteam
sudo groupadd labteam
sudo usermod -aG labteam labreader
id labreader
id -nG labreader | grep -qw labteam
''',user='root',note='Expected absent-account queries asserted; administrator steps as root')
 t('08 permissions',['08-01','08-02','08-03'],B('08-01')+'''
chmod u-w note.txt
if printf bad >> note.txt; then exit 1; fi
chmod u+w note.txt
mkdir private; chmod 700 private; ls -ld private
test "$(stat -c %a note.txt)" = 600
test "$(stat -c %a private)" = 700
umask; (umask 022; touch mask-file; mkdir mask-dir)
test "$(stat -c %a mask-file)" = 644
test "$(stat -c %a mask-dir)" = 755
printf data > readonly; chmod 444 readonly; rm -f readonly; test ! -e readonly
''')
 t('08 other account read denied',[],'cat /home/eulercheck/linux-lab/permissions/note.txt',user='labreader',cwd='/tmp',expected=1)
 t('09 queries',['09-01','09-02','09-03'],B('09-01')+'\ndnf info vim-enhanced\n'+B('09-03')+'\nrpm -qf /usr/bin/vim',timeout=240,note='Installation executed separately with reviewed transaction')
 t('09 update exit code',[],'''set +e
dnf check-update > "$HOME/check-update.txt" 2>&1
status=$?
set -e
tail -n 10 "$HOME/check-update.txt"
printf 'check-update exit=%s\n' "$status"
test "$status" -eq 0 || test "$status" -eq 100
''',timeout=240)
 t('10 jobs and TERM',['10-01','10-02','10-03'],'''sleep 120 &
lab_pid=$!
trap 'kill -TERM "$lab_pid" 2>/dev/null || true' EXIT
printf '%s\n' "$lab_pid"
ps -p "$lab_pid" -o pid,ppid,stat,comm
jobs
test "$(jobs -p)" = "$lab_pid"
kill -TERM "$lab_pid"
wait "$lab_pid" || test "$?" -eq 143
! ps -p "$lab_pid"
trap - EXIT
''',note='Only newly created sleep PID stopped')
 t('11 systemd',['11-01'],B('11-01'))
 t('11 ssh unit journal',['11-02'],B('11-02'),user='root')
 t('12 network',['12-01','12-02','12-03'],B('12-01','12-02','12-03'),timeout=60)
 t('13 host fingerprint',['13-02'],B('13-02'),user='root')
 t('14 archives',['14-01','14-02','14-03'],B('14-01','14-02','14-03')+'''
cmp source/b.txt restore/b.txt
mkdir restore2; tar -xzf notes.tar.gz -C restore2
cmp source/a.txt restore2/a.txt
printf changed >> notes.tar.gz
if sha256sum -c notes.tar.gz.sha256; then exit 1; fi
''',note='Includes corruption detection on test archive')
 t('15 storage',['15-01','15-02'],B('15-01','15-02'))
 t('15 pre-mount',['15-03'],'''mkdir -p ~/linux-lab/mount-demo
ls -la ~/linux-lab/mount-demo
if findmnt --mountpoint "$HOME/linux-lab/mount-demo"; then exit 1; fi
''')
 t('15 tmpfs',['15-04'],'''trap 'umount /home/eulercheck/linux-lab/mount-demo 2>/dev/null || true' EXIT
'''+B('15-04')+'''
! findmnt --mountpoint "$HOME/linux-lab/mount-demo"
trap - EXIT
''',user='root',note='Only new empty mountpoint; EXIT trap also unmounts on failure')
 t('16 environment',['16-01','16-02','16-03','16-04'],B('16-01')+'''
test "$(bash -c 'printf "%s" "$lab_message"')" = ''
export lab_message
test "$(bash -c 'printf "%s" "$lab_message"')" = 'hello environment'
bash -c 'lab_message=child'
test "$lab_message" = 'hello environment'
unset lab_message
'''+B('16-03','16-04'))
 t('17 streams',['17-01','17-02','17-03','17-04','17-05','17-06'],B('17-01')+'''
ls result.txt missing.txt > out.txt 2> err.txt || test "$?" -eq 2
test "$(cat out.txt)" = result.txt; grep -q missing.txt err.txt
ls result.txt missing.txt > combined.txt 2>&1 || test "$?" -eq 2
grep -q result.txt combined.txt; grep -q missing.txt combined.txt
'''+B('17-04','17-05','17-06')+'''
test "$(wc -l < captured.txt)" -eq 2
grep -Fx 'path=$HOME' example.conf
bash -c 'printf out; printf err >&2' > first.txt 2>&1
test "$(cat first.txt)" = outerr
''')
 t('18 search',['18-01','18-02','18-03','18-05'],B('18-01','18-02','18-03','18-05')+'''
printf 'ERROR spaced\n' > 'space name.log'
find . -type f -name '*.log' -exec grep -nH -F 'ERROR' {} + > matches.txt
grep -F 'space name.log:1:ERROR spaced' matches.txt
if printf ' WARN\n' | grep -E '^(WARN|ERROR)'; then exit 1; fi
''')
 put(LAB/'scripts/hello.sh',B('19-02')+'\n')
 put(LAB/'scripts/count-lines.sh',B('19-05')+'\n')
 put(LAB/'scripts/readable.sh',B('19-04')+'\n')
 put(LAB/'scripts/loop.sh',B('19-06')+'\n')
 t('19 invocation',['19-01','19-02','19-03'],'cd ~/linux-lab/scripts\n'+B('19-03'),note='File uses exact manuscript content; editing tested separately')
 t('19 error branches',['19-05'],'''cd ~/linux-lab/scripts
if bash count-lines.sh; then exit 1; else test "$?" -eq 2; fi
if bash count-lines.sh missing; then exit 1; else test "$?" -eq 1; fi
printf 'a\nb\n' > 'two lines.txt'
test "$(bash count-lines.sh 'two lines.txt')" = '2 two lines.txt'
''')
 t('19 snippets',['19-04','19-06','19-07'],'''cd ~/linux-lab/scripts
bash readable.sh 'two lines.txt'
if bash readable.sh missing; then exit 1; else test "$?" -eq 1; fi
bash loop.sh 'two lines.txt' missing
'''+B('19-07')+'''\nshow_file 'two lines.txt'
''')
 for name in ['backup-notes.sh','check-health.sh','wait-ready.sh']:put(LAB/'scripts'/name,(BASE/'examples'/name).read_text())
 t('20 backup restore',['20-01','20-02','20-03'],B('20-01','20-03')+'''
archive=$(find "$HOME/linux-lab/backups" -name notes.tar.gz | head -n1)
mkdir "$HOME/linux-lab/backup-restore"
tar -xzf "$archive" -C "$HOME/linux-lab/backup-restore"
cmp "$HOME/linux-lab/notes/day1.txt" "$HOME/linux-lab/backup-restore/day1.txt"
test "$(stat -c %a "$(dirname "$archive")")" = 700
''')
 t('20 missing source',[],'''mv "$HOME/linux-lab/notes" "$HOME/linux-lab/notes.saved"
trap 'mv "$HOME/linux-lab/notes.saved" "$HOME/linux-lab/notes"' EXIT
if bash "$HOME/linux-lab/scripts/backup-notes.sh"; then exit 1; else test "$?" -eq 1; fi
''')
 t('20 connection failure',['20-04'],'if bash ~/linux-lab/scripts/check-health.sh; then exit 1; else test "$?" -eq 1; fi')
 t('21 Git',['21-01','21-02','21-03'],B('21-01','21-02')+'''
git config user.name 'Hola Euler Test'
git config user.email 'test@example.invalid'
git commit -m 'Create lab project'
printf '%s\n' 'second revision' >> README.md
if git diff --exit-code; then exit 1; fi
git add README.md; git commit -m 'Revise lab project'
test "$(git rev-list --count HEAD)" -eq 2
touch build/generated.class logs/test.log
git check-ignore build/generated.class logs/test.log
test -z "$(git status --porcelain)"
''',note='Repository-local test identity replaces placeholders')
if __name__=='__main__':
 foundation()
 print(json.dumps({'cases':len(results),'passed':sum(r['passed'] for r in results),'failed':[r['name'] for r in results if not r['passed']]}))
