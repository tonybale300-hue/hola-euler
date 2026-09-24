"""Build the private review edition from the shared manuscript."""
from pathlib import Path
import re,html,json,os,argparse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,
    PageBreak,Flowable,LongTable,TableStyle,KeepTogether,CondPageBreak)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing,Rect,Line,String,Polygon
from reportlab.graphics import renderPDF,renderSVG
import math

B=Path(__file__).resolve().parents[1]
VERSION=(B/'VERSION').read_text(encoding='utf-8').strip()
OUT=B/'downloads'/VERSION/f'Hola-Euler-{VERSION}.pdf'
W,H=170*mm,240*mm
M=42
CW=W-2*M
GREEN=colors.HexColor('#438734')
DARK=colors.HexColor('#172321')
MUTED=colors.HexColor('#64716A')
PALE=colors.HexColor('#F0F5ED')
LINE=colors.HexColor('#D8E2D4')
FONTDIR=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
pdfmetrics.registerFont(TTFont('CN',str(FONTDIR/'simsun.ttc'),subfontIndex=0))
pdfmetrics.registerFont(TTFont('CNHead',str(FONTDIR/'simhei.ttf')))
pdfmetrics.registerFont(TTFont('Mono',str(FONTDIR/'consola.ttf')))
pdfmetrics.registerFontFamily('CN',normal='CN',bold='CNHead',italic='CN',boldItalic='CNHead')

styles={
 'body':ParagraphStyle('Body',fontName='CN',fontSize=10.4,leading=16.7,textColor=DARK,spaceAfter=7,wordWrap='CJK',splitLongWords=True,allowWidows=0,allowOrphans=0),
 'h1':ParagraphStyle('H1',fontName='CNHead',fontSize=22,leading=31,textColor=DARK,spaceBefore=10,spaceAfter=20,keepWithNext=True,wordWrap='CJK'),
 'h2':ParagraphStyle('H2',fontName='CNHead',fontSize=14.2,leading=22,textColor=GREEN,spaceBefore=14,spaceAfter=8,keepWithNext=True,wordWrap='CJK'),
 'h3':ParagraphStyle('H3',fontName='CNHead',fontSize=11.2,leading=18,textColor=DARK,spaceBefore=8,spaceAfter=6,keepWithNext=True,wordWrap='CJK'),
 'note':ParagraphStyle('Note',fontName='CN',fontSize=9.5,leading=16,textColor=DARK,spaceAfter=10,spaceBefore=5,borderColor=LINE,borderWidth=.7,borderPadding=10,backColor=PALE,wordWrap='CJK'),
 'list':ParagraphStyle('List',fontName='CN',fontSize=10.1,leading=17.5,textColor=DARK,leftIndent=10,firstLineIndent=-10,spaceAfter=7,wordWrap='CJK',allowWidows=0,allowOrphans=0),
 'cell':ParagraphStyle('Cell',fontName='CN',fontSize=8.9,leading=14.4,textColor=DARK,wordWrap='CJK'),
 'cellhead':ParagraphStyle('CellHead',fontName='CNHead',fontSize=9,leading=14.5,textColor=colors.white,wordWrap='CJK'),
 'caption':ParagraphStyle('Caption',fontName='CN',fontSize=8.6,leading=13,textColor=MUTED,spaceAfter=10,wordWrap='CJK')
}

def inline(s):
    # Escape all prose before introducing controlled ReportLab link markup.
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{m[2]}" color="#438734">{m[1]}</link>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Mono">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',s)
    return s

def font_for(ch):return 'CN' if ord(ch)>127 else 'Mono'
def text_width(s,size):return sum(pdfmetrics.stringWidth(c,font_for(c),size) for c in s)
def mono_text(c,x,y,s,size):
    for ch in s:
        f=font_for(ch);c.setFont(f,size);c.drawString(x,y,ch);x+=pdfmetrics.stringWidth(ch,f,size)

class Code(Flowable):
    def __init__(self,lines,lang='',continued=False,size=None):
        super().__init__();self.lines=lines;self.lang=lang;self.continued=continued
        longest=max((text_width(x,8.2) for x in lines),default=1)
        self.size=size or min(8.2,8.2*(CW-24)/max(longest,1))
        if self.size<6.5:raise ValueError('Code line too wide: '+max(lines,key=len))
        self.leading=self.size*1.4;self.width=CW
        self.height=27+len(lines)*self.leading
        self.spaceBefore=3;self.spaceAfter=11
    def wrap(self,aw,ah):return self.width,self.height
    def split(self,aw,ah):
        n=int((ah-27)/self.leading)
        if n<4:return []
        if len(self.lines)-n<3:n=len(self.lines)-3
        if n<4:return []
        return [Code(self.lines[:n],self.lang,self.continued,self.size),Code(self.lines[n:],self.lang,True,self.size)]
    def draw(self):
        c=self.canv;c.setFillColor(colors.HexColor('#F2F4F3'));c.setStrokeColor(LINE)
        c.roundRect(0,0,self.width,self.height,5,fill=1,stroke=1)
        c.setFillColor(GREEN);c.setFont('Mono',6.8)
        label=(self.lang or 'text').upper()+(' / CONTINUED' if self.continued else '')
        c.drawString(11,self.height-12,label)
        c.setFillColor(DARK);y=self.height-25
        for line in self.lines:
            mono_text(c,11,y,line,self.size);y-=self.leading

DIAGRAMS={
'layers':('图 1-1 从应用到硬件',[['应用程序','Bash 与常用工具'],['系统调用','Linux 内核'],['硬件','CPU / 内存 / 磁盘']]),
'shell':('图 2-1 一条命令的工作过程',[['终端','接收键盘输入'],['Bash','解析与展开参数'],['程序与内核','执行并返回结果']]),
'tree':('图 3-1 从根目录展开',[['/','目录树起点'],['/home/alex','个人文件'],['/etc   /var   /usr','配置 / 变化数据 / 系统资源']]),
'paths':('图 3-2 同一个位置的两种写法',[['当前目录','/home/alex/linux-lab'],['相对路径','paths/notes'],['最终位置','/home/alex/linux-lab/paths/notes']]),
'copy':('图 4-1 复制保留源文件',[['复制前','hello.txt'],['cp hello.txt backup.txt','读取源并写出目标'],['复制后','hello.txt 与 backup.txt']]),
'links':('图 4-2 名称与文件对象',[['original.txt + hard.txt','两个名称关联同一 inode'],['soft.txt','保存路径 original.txt'],['移除 original.txt 后','hard.txt 仍可访问；soft.txt 可能失效']]),
'users':('图 7-1 身份与组关系',[['用户','UID 标识账户'],['主组 + 附加组','多个 GID 参与权限判断'],['文件对象','所有者 / 所属组 / 权限']]),
'permissions':('图 8-1 把权限拆成三组',[['所有者 u','rw- = 4 + 2 = 6'],['所属组 g','r-- = 4 = 4'],['其他人 o','--- = 0；组合后为 640']]),
'process':('图 10-1 进程关系与标识',[['Bash','父进程'],['sleep 120','子进程，获得自己的 PID'],['PPID','记录父进程的 PID']]),
'service':('图 11-1 服务管理关系',[['单元文件','路径 / 身份 / 启动命令'],['systemd','读取定义并管理进程'],['应用进程 + journal','运行状态与日志证据']]),
'network':('图 12-1 一次请求经过的对象',[['客户端','DNS 查询与目标地址'],['网络路径','接口 / 路由 / 允许的流量'],['服务器','监听端口与应用处理']]),
'ssh':('图 13-1 本地转发的两端',[['电脑 127.0.0.1:18080','客户端浏览器入口'],['加密 SSH 连接','通过已验证的服务器'],['服务器 127.0.0.1:8080','应用只监听服务器本机']]),
'storage':('图 15-1 路径怎样连接到存储',[['磁盘 / 分区 / 逻辑卷','提供块存储区域'],['文件系统','组织数据与元数据'],['挂载点','接到目录树中的路径']]),
'pathlookup':('图 16-1 PATH 的目录次序',[['输入外部命令名','先完成 Shell 自身的解析'],['PATH 中的目录','按配置次序查找'],['匹配的可执行程序','路径确定后启动']]),
'streams':('图 17-1 三个标准描述符',[['0 / stdin','标准输入，程序从这里读'],['1 / stdout','标准输出，写正常结果'],['2 / stderr','标准错误，写诊断信息']]),
'pipeline':('图 17-2 排序与统计的管道',[['printf','产生文本行'],['sort','读入并排序'],['uniq -c','统计相邻重复组']]),
'deploy':('图 23-1 发布目录与可写数据',[['/opt/labapp/releases/v1','root 管理的程序版本'],['/opt/labapp/current','指向当前版本的软链接'],['/var/lib/labapp','labapp 可写的数据目录']]),
'vim-modes':('图 6-1 输入之前先认模式',[['普通模式','移动 / 删除 / 撤销'],['插入模式','把按键写成正文'],['命令行模式','保存 / 退出 / 替换']]),
'redirection-order':('图 17-3 重定向顺序改变目标',[['先改 1，再复制给 2','cmd >file 2>&1'],['先复制 1，再单独改 1','cmd 2>&1 >file'],['复制保存当时的目标','后面的改变不会自动跟随']]),
'release-cycle':('图 24-1 版本切换与恢复',[['v1 运行','current 指向 releases/v1'],['v2 验证','停止 / 换链接 / 启动 / 等待'],['回滚 v1','再次启动并核对响应中的版本']]),
}

class Diagram(Flowable):
    def __init__(self,key):
        super().__init__();self.key=key;self.width=CW;self.height=192;self.spaceBefore=7;self.spaceAfter=13
    def wrap(self,aw,ah):return self.width,self.height
    def drawing(self):
        d=Drawing(self.width,self.height);title,rows=DIAGRAMS[self.key]
        d.add(Rect(0,0,self.width,self.height,rx=6,ry=6,fillColor=PALE,strokeColor=None))
        def txt(x,y,s,size=9,font='CN',color=DARK):d.add(String(x,y,s,fontName=font,fontSize=size,fillColor=color))
        def box(x,y,w,h,a,b=''):
            d.add(Rect(x,y,w,h,rx=4,ry=4,fillColor=colors.white,strokeColor=LINE,strokeWidth=.7))
            txt(x+8,y+h-15,a,9.5,'CNHead')
            if b:txt(x+8,y+9,b,8.5,'CN',MUTED)
        def arrow(x1,y1,x2,y2):
            d.add(Line(x1,y1,x2,y2,strokeColor=GREEN,strokeWidth=1))
            a=math.atan2(y2-y1,x2-x1);sz=5
            pts=[x2,y2,x2-sz*math.cos(a-.5),y2-sz*math.sin(a-.5),x2-sz*math.cos(a+.5),y2-sz*math.sin(a+.5)]
            d.add(Polygon(pts,fillColor=GREEN,strokeColor=None))
        txt(12,self.height-20,title,10,'CNHead',GREEN)
        if self.key=='tree':
            box(164,128,65,28,'/');
            for x,name in [(14,'/home'),(110,'/etc'),(206,'/var'),(302,'/usr')]:
                arrow(197,128,x+39,108);box(x,79,78,29,name)
            arrow(53,79,90,58);box(14,16,228,42,'/home/alex/linux-lab','个人实验目录从 /home 分支向下展开')
        elif self.key=='links':
            box(13,123,100,28,'original.txt');box(13,78,100,28,'hard.txt')
            box(162,111,88,37,'同一 inode');box(288,111,95,37,'文件内容')
            arrow(113,136,162,134);arrow(113,92,162,123);arrow(250,129,288,129)
            box(13,20,100,31,'soft.txt');box(162,17,221,39,'保存路径 original.txt','解析这个路径，再到达文件对象')
            arrow(113,35,162,35)
        elif self.key=='permissions':
            for x,a,b,c in [(13,'所有者 u','rw-','4 + 2 = 6'),(143,'所属组 g','r--','4 = 4'),(273,'其他人 o','---','0')]:
                box(x,51,112,96,a);txt(x+17,96,b,22,'Mono',GREEN);txt(x+14,69,c,11,'Mono')
            txt(18,24,'普通文件类型 - 与三组权限分开看。组合示例为 640。',9)
        elif self.key=='streams':
            box(13,73,104,42,'0 / stdin','输入内容');box(159,73,76,42,'程序')
            box(279,113,105,42,'1 / stdout','正常结果');box(279,31,105,42,'2 / stderr','诊断信息')
            arrow(117,94,159,94);arrow(235,101,279,132);arrow(235,86,279,53)
            txt(16,13,'每个编号都可以连接终端、文件或其他合适的对象。',8.5)
        elif self.key=='pipeline':
            for x,a,b in [(13,'printf','产生文本'),(146,'sort','排序'),(279,'uniq -c','相邻计数')]:box(x,71,105,63,a,b)
            arrow(118,102,146,102);arrow(251,102,279,102)
            txt(16,39,'箭头连接前一程序的 stdout 与后一程序的 stdin。',9)
            txt(16,21,'普通管道不会自动把 stderr 合并进来。',9)
        elif self.key=='deploy':
            box(13,117,204,39,'/opt/labapp/current','软链接，只指向当前版本');box(262,117,121,39,'releases/v1','root 管理')
            arrow(217,137,262,137)
            box(13,32,370,58,'/var/lib/labapp','独立的数据目录，由 labapp 写入；不随 current 一起切换')
        elif self.key=='vim-modes':
            box(12,65,108,54,'普通模式','命令键改变文本')
            box(257,112,127,43,'插入模式','输入文字')
            box(257,30,127,43,'命令行模式',':w / :q / :%s')
            arrow(120,106,257,138);txt(176,133,'i',10,'Mono',GREEN)
            arrow(257,118,120,90);txt(173,103,'Esc',9,'Mono')
            arrow(120,78,257,52);txt(171,57,':',11,'Mono',GREEN)
            arrow(257,38,120,66);txt(153,29,'Esc / 执行后返回',8)
        elif self.key=='redirection-order':
            for y,label,left,right in [(117,'cmd >file 2>&1','1 → file','2 → file'),(57,'cmd 2>&1 >file','1 → file','2 → 终端')]:
                box(13,y-14,370,47,label)
                txt(190,y+3,left,9);txt(284,y+3,right,9)
            txt(18,15,'从左到右安排输出，2 复制的是当时 1 的目标。',9)
        elif self.key=='release-cycle':
            box(13,100,104,51,'v1 运行','核对 v1 响应')
            box(145,100,110,51,'v2 运行','核对 v2 响应')
            box(282,100,104,51,'v1 恢复','再次核对响应')
            arrow(117,126,145,126);arrow(255,126,282,126)
            box(13,26,373,47,'每次切换都要停、换、启、查','停止进程 → 切换链接 → 启动 → 有限等待并检查版本')
        else:
            for i,(a,b) in enumerate(rows):
                y=self.height-70-i*51
                box(13,y,self.width-26,40,a,b)
                if i<2:arrow(self.width/2,y-1,self.width/2,y-10)
        return d
    def draw(self):
        renderPDF.draw(self.drawing(),self.canv,0,0)

class Cover(Flowable):
    def __init__(self):super().__init__();self.width=CW;self.height=H-105
    def draw(self):
        c=self.canv;c.saveState()
        # The cover flowable origin is the content frame's lower left.
        c.translate(-M,-46)
        cover=B/'assets/cover/hola-euler.png'
        if cover.exists():
            c.setFillColor(colors.white);c.rect(0,0,W,H,fill=1,stroke=0)
            c.drawImage(str(cover),0,0,width=W,height=H,preserveAspectRatio=True,anchor='c')
            c.restoreState();return
        c.setFillColor(colors.HexColor('#FAFBF7'));c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(GREEN);c.rect(0,0,12,H,fill=1,stroke=0)
        c.setFillColor(DARK);c.setFont('CN',11)
        c.drawString(44,H-63,'从 0 开始，用命令行打开更大的世界。')
        c.setStrokeColor(GREEN);c.setLineWidth(2);c.line(44,H-79,104,H-79)
        c.setFont('Helvetica-Bold',83);c.setFillColor(DARK);c.drawString(39,H-195,'H')
        c.setFillColor(GREEN);c.drawString(99,H-195,'o')
        c.setFillColor(DARK);c.drawString(150,H-195,'la')
        c.setFont('Helvetica-Bold',87);c.drawString(38,H-280,'Euler')
        c.setFillColor(GREEN);c.setFont('Mono',42);c.drawString(322,H-272,'>_')
        c.setFont('CNHead',19);c.setFillColor(DARK);c.drawString(44,H-326,'openEuler Linux')
        c.setFont('CNHead',21);c.drawString(44,H-357,'从命令行到服务器实战')
        c.setFont('CNHead',14);c.drawString(44,H-403,'Alex 著')
        c.setFillColor(MUTED);c.setFont('CN',10);c.drawString(44,H-426,'写给每一个想真正学会 Linux 的你')
        c.setFillColor(DARK);c.roundRect(44,93,W-88,110,7,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#9BD379'));c.setFont('Mono',11)
        c.drawString(60,179,'$ mkdir -p ~/linux-lab')
        c.drawString(60,159,'$ cd ~/linux-lab')
        c.drawString(60,139,'$ pwd')
        c.setFillColor(colors.white);c.setFont('CN',10);c.drawString(60,115,'从第一个目录，到一次完整部署。')
        c.setFillColor(GREEN);c.setFont('CNHead',10);c.drawString(44,65,'作者批阅初稿  /  v0.1-review')
        c.setFillColor(MUTED);c.setFont('CN',8.5);c.drawString(44,45,'openEuler 24.03 LTS SP4 · x86_64 · Bash')
        c.restoreState()

class BookDoc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(str(path),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=45,bottomMargin=43,
            title='Hola Euler | openEuler Linux 从命令行到服务器实战',author='Alex',subject=f'修订审阅版 {VERSION}',allowSplitting=True)
        self.addPageTemplates(PageTemplate(id='normal',frames=[Frame(M,43,CW,H-88,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPageEnd=self.page))
        self.current='';self.headings=[]
    def beforeDocument(self):self.current='';self.headings=[]
    def page(self,c,d):
        if d.page==1:return
        c.saveState();c.setStrokeColor(LINE);c.line(M,H-28,W-M,H-28)
        c.setFillColor(MUTED);c.setFont('CN',8);c.drawString(M,H-20,'Hola Euler · Alex')
        title=self.current
        while pdfmetrics.stringWidth(title,'CN',8)>CW-110:title=title[:-1]
        c.drawRightString(W-M,H-20,title)
        c.setFont('CN',7.5);c.drawString(M,23,f'{VERSION} · 修订审阅版 · 实测状态见验证说明')
        c.setFont('Mono',8);c.drawRightString(W-M,23,f'{d.page:03d}')
        c.restoreState()
    def afterFlowable(self,f):
        if hasattr(f,'header_current'):self.current=f.header_current
        if hasattr(f,'heading_level'):
            level=f.heading_level;text=f.getPlainText();key=f.key
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text,key,level=level,closed=(level>0))
            self.notify('TOCEntry',(level,text,self.page,key))
            self.headings.append({'level':level,'title':text,'page':self.page,'key':key})
            if level==0:self.current=text

counter=0
def heading(text,level):
    global counter
    counter+=1
    p=Paragraph(inline(text),styles[f'h{level+1}']);p.heading_level=level;p.key=f'h{counter:04d}'
    return p

def table(rows):
    n=len(rows[0]);widths=([CW*.36,CW*.49,CW*.15] if n==3 else [CW*.34,CW*.66]) if n in (2,3) else [CW/n]*n
    if n==3 and rows[0][-1]=='记忆重点':widths=[CW*.25,CW*.43,CW*.32]
    if n==4:widths=[CW*.18,CW*.27,CW*.28,CW*.27]
    cells=[[Paragraph(inline(cell),styles['cellhead' if i==0 else 'cell']) for cell in row] for i,row in enumerate(rows)]
    t=LongTable(cells,colWidths=widths,repeatRows=1,hAlign='LEFT',spaceBefore=5,spaceAfter=12)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),GREEN),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),('LINEBELOW',(0,0),(-1,-1),.4,LINE),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
    return t

def parse(text):
    lines=text.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            lang=line[3:];buf=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):buf.append(lines[i]);i+=1
            out.append(Code(buf,lang));i+=1;continue
        if line.startswith(':::diagram '):out.append(Diagram(line.split()[-1]));i+=1;continue
        figure=re.fullmatch(r'!\[[^\]]*\]\(\.\./assets/diagrams/([\w-]+)\.svg\)',line)
        if figure:out.append(Diagram(figure[1]));i+=1;continue
        m=re.match(r'^(#{1,3}) (.*)',line)
        if m:
            level=len(m[1])-1
            if level==0:out.append(PageBreak())
            out.append(heading(m[2],level));i+=1;continue
        if line.startswith('|') and line.endswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                row=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',x) for x in row):rows.append(row)
                i+=1
            out.append(table(rows));continue
        if line.startswith('> '):out.append(KeepTogether([Paragraph(inline(line[2:]),styles['note'])]));i+=1;continue
        if line.startswith('- '):out.append(Paragraph('• '+inline(line[2:]),styles['list']));i+=1;continue
        if re.match(r'^\d+\. ',line):out.append(Paragraph(inline(line),styles['list']));i+=1;continue
        buf=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|:::|\||> |\- |\d+\. )',lines[i]):buf.append(lines[i]);i+=1
        style=styles['caption'] if line.startswith('资料依据') else styles['body']
        p=Paragraph(inline(' '.join(buf)),style)
        if line.startswith('资料依据') and out and isinstance(out[-1],Paragraph):out[-1].keepWithNext=True
        out.append(p)
    for pos,flow in enumerate(out):
        if isinstance(flow,Paragraph) and '本章练习' in flow.getPlainText():
            out=out[:pos]+[KeepTogether(out[pos:])]
            break
    return out

def main():
    global OUT
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    if args.output:OUT=args.output
    OUT.parent.mkdir(parents=True,exist_ok=True)
    story=[Cover()]
    story+=parse((B/'frontmatter.md').read_text(encoding='utf-8'))
    story.append(PageBreak());toc_title=Paragraph('目录',styles['h1']);toc_title.header_current='目录';story.append(toc_title)
    story.append(Paragraph('三级目录 · 可点击跳转 · 页码为 PDF 页序',styles['caption']))
    toc=TableOfContents();toc.dotsMinLevel=0
    toc.levelStyles=[
        ParagraphStyle('T0',fontName='CNHead',fontSize=10.5,leading=17,spaceBefore=8,textColor=GREEN,leftIndent=0,firstLineIndent=0),
        ParagraphStyle('T1',fontName='CN',fontSize=9,leading=14.5,leftIndent=12,firstLineIndent=0),
        ParagraphStyle('T2',fontName='CN',fontSize=8.2,leading=13,leftIndent=23,firstLineIndent=0,textColor=MUTED)
    ]
    story.append(toc)
    for p in sorted((B/'chapters').glob('*.md')):story+=parse(p.read_text(encoding='utf-8'))
    story+=parse((B/'answers/answers.md').read_text(encoding='utf-8'))
    for p in sorted((B/'appendices').glob('*.md')):story+=parse(p.read_text(encoding='utf-8'))
    story+=parse((B/'SOURCES.md').read_text(encoding='utf-8'))
    doc=BookDoc(OUT);doc.multiBuild(story,maxPasses=5)
    (B/'review/page-map.json').write_text(json.dumps(doc.headings,ensure_ascii=False,indent=2),encoding='utf-8')
    # Standalone original vector diagrams for later editing/reuse.
    for key in DIAGRAMS:
        dest=B/'assets/diagrams'/f'{key}.svg'
        renderSVG.drawToFile(Diagram(key).drawing(),str(dest))
        svg=dest.read_text(encoding='utf-8').replace('font-family: CNHead','font-family: SimHei').replace('font-family: CN','font-family: SimSun').replace('font-family: Mono','font-family: Consolas')
        dest.write_text(svg,encoding='utf-8')
    print(OUT)
    print('headings',len(doc.headings),'pages',doc.page)

if __name__=='__main__':main()
