"""Build an EPUB 3 from the same Markdown sources as the PDF (stdlib only)."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
from xml.etree import ElementTree as ET
import argparse, html, re, hashlib

B = Path(__file__).resolve().parents[1]
XHTML = 'http://www.w3.org/1999/xhtml'
CSS = '''body{font-family:serif;line-height:1.75;color:#172321;margin:5%;}
h1,h2,h3{font-family:sans-serif;line-height:1.4;break-after:avoid;}h1,h2{color:#438734;}
h1{font-size:1.7em;}h2{font-size:1.35em;}h3{font-size:1.1em;}
p{margin:.65em 0;}a{color:#367329;}pre{white-space:pre-wrap;overflow-wrap:anywhere;
font-family:monospace;font-size:.8em;background:#f2f4f3;padding:1em;border:1px solid #d8e2d4;}
code{font-family:monospace;}aside{border-left:.25em solid #438734;background:#f0f5ed;
padding:.6em 1em;margin:1em 0;break-inside:avoid;}figure{margin:1em 0;break-inside:avoid;}
img{max-width:100%;height:auto;}figcaption{font-size:.85em;color:#64716a;}
table{border-collapse:collapse;width:100%;font-size:.85em;}th,td{border:1px solid #d8e2d4;
padding:.4em;vertical-align:top;}th{background:#f0f5ed;}li{margin:.4em 0;}
.cover{text-align:center;margin:0;}.cover img{max-height:95vh;}'''

def inline(s):
    escaped=html.escape(s,quote=False)
    escaped=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:'<a href="'+html.escape(html.unescape(m[2]),quote=True)+'">'+m[1]+'</a>',escaped)
    escaped=re.sub(r'`([^`]+)`',r'<code>\1</code>',escaped)
    return re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',escaped)

def render(text):
    lines=text.splitlines(); out=[]; heads=[]; images=set(); i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip(): i+=1;continue
        if line.startswith('```'):
            code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            if i==len(lines):raise ValueError('Unclosed code fence')
            out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>');i+=1;continue
        match=re.match(r'^(#{1,3}) (.+)',line)
        if match:
            level=len(match[1]);key='h'+str(len(heads)+1);heads.append((level,match[2],key))
            out.append(f'<h{level} id="{key}">{inline(match[2])}</h{level}>');i+=1;continue
        figure=re.fullmatch(r'!\[[^\]]*\]\(\.\./assets/diagrams/([\w-]+)\.svg\)',line)
        if line.startswith(':::diagram ') or figure:
            key=figure[1] if figure else line.split()[-1];images.add(key)
            # SVG is an EPUB core media type. Text alternative survives image suppression.
            alt=diagram_caption(key)
            out.append(f'<figure><img src="images/{key}.svg" alt="{html.escape(alt,quote=True)}"/><figcaption>{inline(alt)}</figcaption></figure>');i+=1;continue
        if line.startswith('|') and line.endswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|') and lines[i].endswith('|'):
                row=[c.strip() for c in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',c) for c in row):rows.append(row)
                i+=1
            out.append('<table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table>');continue
        if line.startswith('> '):out.append('<aside>'+inline(line[2:])+'</aside>');i+=1;continue
        if line.startswith('- ') or re.match(r'^\d+\. ',line):
            ordered=bool(re.match(r'^\d+\. ',line));tag='ol' if ordered else 'ul';items=[]
            while i<len(lines) and (bool(re.match(r'^\d+\. ',lines[i])) if ordered else lines[i].startswith('- ')):
                items.append(re.sub(r'^(?:\d+\. |- )','',lines[i]));i+=1
            out.append('<'+tag+'>'+''.join('<li>'+inline(x)+'</li>' for x in items)+'</'+tag+'>');continue
        buf=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|:::|> |- |\d+\. )',lines[i]):
            if lines[i].startswith('|') and lines[i].endswith('|'):break
            buf.append(lines[i]);i+=1
        out.append('<p>'+inline(' '.join(buf))+'</p>')
    return '\n'.join(out),heads,images

def diagram_caption(key):
    # Read the title from the exported SVG without importing the PDF/font runtime.
    root=ET.parse(B/'assets/diagrams'/f'{key}.svg').getroot()
    texts=[''.join(e.itertext()) for e in root.iter() if e.tag.endswith('}text')]
    return next((s for s in texts if s.startswith('图 ')),key)

def document(title,body):
    return '<?xml version="1.0" encoding="utf-8"?>\n'+f'<html xmlns="{XHTML}" xmlns:epub="http://www.idpf.org/2007/ops" lang="zh-CN" xml:lang="zh-CN"><head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>{body}</body></html>'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--version',default=None);parser.add_argument('--output',type=Path);args=parser.parse_args()
    version=args.version or (B/'VERSION').read_text().strip()
    output=args.output or B/'downloads'/version/f'Hola-Euler-{version}.epub'
    output.parent.mkdir(parents=True,exist_ok=True)
    sources=[B/'frontmatter.md',*sorted((B/'chapters').glob('*.md')),B/'answers/answers.md',*sorted((B/'appendices').glob('*.md')),B/'SOURCES.md']
    files={'style.css':CSS,'cover.xhtml':document('封面','<div class="cover"><img src="images/cover.png" alt="Hola Euler，Alex 著，openEuler Linux 从入门到实战"/></div>')}
    manifest=['<item id="css" href="style.css" media-type="text/css"/>','<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>','<item id="cover-image" href="images/cover.png" media-type="image/png" properties="cover-image"/>']
    spine=['<itemref idref="cover"/>'];nav=['<li><a href="cover.xhtml">封面</a></li>'];allimages=set();ncx=[]
    for idx,p in enumerate(sources):
        body,heads,imgs=render(p.read_text(encoding='utf-8'));name=f'section-{idx:02d}.xhtml';ident=f's{idx}';title=heads[0][1]
        files[name]=document(title,body);allimages|=imgs
        manifest.append(f'<item id="{ident}" href="{name}" media-type="application/xhtml+xml"/>');spine.append(f'<itemref idref="{ident}"/>')
        children=''.join(f'<li><a href="{name}#{key}">{inline(text)}</a></li>' for level,text,key in heads[1:] if level<=2)
        nav.append(f'<li><a href="{name}">{inline(title)}</a>'+('<ol>'+children+'</ol>' if children else '')+'</li>')
        ncx.append(f'<navPoint id="n{idx+1}" playOrder="{idx+1}"><navLabel><text>{html.escape(title)}</text></navLabel><content src="{name}"/></navPoint>')
    files['nav.xhtml']=document('目录','<nav epub:type="toc" id="toc"><h1>目录</h1><ol>'+''.join(nav)+'</ol></nav>')
    manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')
    manifest.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')
    for key in sorted(allimages):manifest.append(f'<item id="img-{key}" href="images/{key}.svg" media-type="image/svg+xml"/>')
    uid='urn:uuid:'+str(__import__('uuid').uuid5(__import__('uuid').NAMESPACE_URL,'hola-euler-alex/'+version))
    files['toc.ncx']=f'<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{uid}"/></head><docTitle><text>Hola Euler</text></docTitle><navMap>'+''.join(ncx)+'</navMap></ncx>'
    opf=f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="zh-CN"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="bookid">{uid}</dc:identifier><dc:title>Hola Euler · openEuler Linux 从入门到实战</dc:title><dc:creator>Alex</dc:creator><dc:language>zh-CN</dc:language><dc:description>{version}，个人学习版；技术验证范围见书内说明。</dc:description><meta property="dcterms:modified">2026-09-25T00:00:00Z</meta><meta name="cover" content="cover-image"/></metadata><manifest>{''.join(manifest)}</manifest><spine toc="ncx">{''.join(spine)}</spine></package>'''
    with ZipFile(output,'w',ZIP_DEFLATED) as z:
        z.writestr('mimetype','application/epub+zip',compress_type=ZIP_STORED)
        z.writestr('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        z.writestr('OEBPS/content.opf',opf)
        for name,content in files.items():z.writestr('OEBPS/'+name,content)
        z.write(B/'assets/cover/hola-euler.png','OEBPS/images/cover.png')
        for key in sorted(allimages):z.write(B/'assets/diagrams'/f'{key}.svg',f'OEBPS/images/{key}.svg')
    print(output)
    print('sections',len(sources),'diagrams',len(allimages),'sha256',hashlib.sha256(output.read_bytes()).hexdigest())

if __name__=='__main__':main()
