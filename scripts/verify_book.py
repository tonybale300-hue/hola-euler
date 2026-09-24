"""Static manuscript/EPUB verification; optional Bash syntax and mocked checks.

Never executes chapter blocks, starts servers, installs packages, or connects to a VM.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_STORED
from xml.etree import ElementTree as ET
import argparse, ast, collections, hashlib, json, re, subprocess, posixpath
from urllib.parse import urlsplit, unquote

B=Path(__file__).resolve().parents[1]

def validate_epub(path):
    with ZipFile(path) as z:
        assert z.testzip() is None
        first=z.infolist()[0]
        assert first.filename=='mimetype' and first.compress_type==ZIP_STORED
        assert z.read('mimetype')==b'application/epub+zip'
        names=set(z.namelist());trees={}
        for name in names:
            if name.endswith(('.xhtml','.xml','.opf','.ncx','.svg')):trees[name]=ET.fromstring(z.read(name))
        opf=trees['OEBPS/content.opf'];ns={'o':'http://www.idpf.org/2007/opf'}
        manifest=opf.find('o:manifest',ns);ids={e.attrib['id'] for e in manifest}
        resources=set()
        for item in manifest:
            target='OEBPS/'+item.attrib['href'];assert target in names,target;resources.add(target)
        assert len(ids)==len(manifest)
        for item in opf.find('o:spine',ns):assert item.attrib['idref'] in ids
        for name,tree in trees.items():
            seen=set()
            for element in tree.iter():
                ident=element.get('id')
                if ident:assert ident not in seen,(name,ident);seen.add(ident)
                for attr in ('href','src'):
                    link=element.get(attr)
                    if not link:continue
                    parts=urlsplit(link)
                    if parts.scheme or parts.netloc:continue
                    dest=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(parts.path))) if parts.path else name
                    assert dest in names,(name,link)
                    if parts.fragment:
                        assert dest in trees
                        assert any(e.get('id')==unquote(parts.fragment) for e in trees[dest].iter()),(name,link)
        return {'entries':len(names),'xml_documents':len(trees),'manifest_resources':len(resources),'checks':'ZIP, XML, manifest, spine, local links and fragments'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--work-dir',type=Path,required=True);parser.add_argument('--bash');args=parser.parse_args()
    work=args.work_dir.resolve();work.mkdir(parents=True,exist_ok=True)
    inventory=[];counts=collections.Counter();syntax=[]
    for p in sorted((B/'chapters').glob('*.md')):
        text=p.read_text(encoding='utf-8');assert text.count('```')%2==0,p
        exercises=[x for x in text.splitlines() if x.startswith('- ') and '｜' in x];assert len(exercises)==6,(p,len(exercises))
        for index,m in enumerate(re.finditer(r'^```([^\n]*)\n(.*?)\n```',text,re.M|re.S),1):
            lang=m[1];code=m[2];line=text[:m.start()].count('\n')+1;counts[lang]+=1
            row={'id':p.stem[:2]+'-'+str(index).zfill(2),'file':p.relative_to(B).as_posix(),'line':line,'language':lang,'sha256':hashlib.sha256(code.encode()).hexdigest(),'review':'静态审查完成；目标系统执行另记','syntax':'not applicable'}
            if lang=='bash':
                f=work/(row['id']+'.sh');f.write_text(code+'\n',encoding='utf-8',newline='\n')
                if args.bash:
                    r=subprocess.run([args.bash,'--noprofile','--norc','-n',str(f)],capture_output=True,text=True)
                    assert r.returncode==0,(row['id'],r.stderr);row['syntax']='Git Bash bash -n passed';syntax.append(row['id'])
                else:row['syntax']='not run this invocation'
            inventory.append(row)
    # Standalone examples must match a complete source block in the manuscript.
    mapping=[('examples/backup-notes.sh','20-script-practice.md','bash'),('examples/check-health.sh','20-script-practice.md','bash'),('examples/wait-ready.sh','24-project.md','bash'),('examples/java-app/LabServer.java','22-java.md','java'),('examples/spring-lab/pom.xml','22-java.md','xml'),('examples/spring-lab/src/main/java/book/alex/LabApplication.java','22-java.md','java'),('examples/spring-lab/src/main/resources/application.properties','22-java.md','properties'),('examples/labapp.service','24-project.md','ini')]
    for example,chapter,lang in mapping:
        snippets=re.findall('```'+lang+r'\n(.*?)\n```',(B/'chapters'/chapter).read_text(encoding='utf-8'),re.S)
        assert (B/example).read_text(encoding='utf-8').strip() in [s.strip() for s in snippets],example
    for p in (B/'scripts').glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    ET.parse(B/'examples/spring-lab/pom.xml')
    version=(B/'VERSION').read_text().strip()
    epub=validate_epub(B/'downloads'/version/f'Hola-Euler-{version}.epub')
    tests=[]
    if args.bash:
        # Inject small shell functions instead of real network calls or sleeping.
        for script,argv,cases in [
            ('check-health.sh',[],[('ok\n\n200',0,0),('failed\n\n200',0,1),('ok\n\n302',0,1),('',7,1)]),
            ('wait-ready.sh',['v2'],[('Hola Euler v2\n\n200',0,0),('Hola Euler v1\n\n200',0,1),('Hola Euler v2\n\n302',0,1),('',7,1)])]:
            for index,(body,curlcode,expected) in enumerate(cases):
                quote=lambda s:"'"+s.replace("'","'\"'\"'")+"'"
                test=work/f'mock-{script}-{index}.sh'
                content='curl() { printf %s '+quote(body)+'; return '+str(curlcode)+'; }\nsleep() { :; }\nexport -f curl sleep\nbash "$@"\n'
                test.write_text(content,encoding='utf-8',newline='\n')
                path=(B/'examples'/script).resolve().as_posix()
                result=subprocess.run([args.bash,'--noprofile','--norc',str(test),path,*argv],capture_output=True,text=True)
                assert result.returncode==expected,(script,index,result.returncode,result.stderr)
                tests.append({'script':script,'case':index,'exit':expected})
        result=subprocess.run([args.bash,'--noprofile','--norc',str(B/'examples/wait-ready.sh')],capture_output=True,text=True)
        assert result.returncode==2;tests.append({'script':'wait-ready.sh','case':'missing argument','exit':2})
    (B/'review/command-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    result={'version':version,'chapters':25,'exercises':150,'code_blocks':len(inventory),'languages':dict(counts),'bash_syntax_pass':len(syntax),'synchronized_examples':len(mapping),'mock_tests':tests,'epub':epub,'openEuler_runtime':'not evaluated by this script; see vm-check-results.json for target-system evidence','java_runtime':'not executed in this revision'}
    (B/'review/static-check-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
