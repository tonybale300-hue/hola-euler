# 构建与检查

在仓库根目录执行。VERSION 是当前电子书版本的唯一来源，下载文件位于 downloads/版本号/。

## PDF

本版排版在 Windows 完成，需要 Python 3、reportlab、pypdf 和 pdfplumber。视觉检查另使用 Pillow 与 Poppler 的 pdftoppm。字体使用本机 Windows Fonts 中的 simsun.ttc、simhei.ttf、consola.ttf，仓库不分发字体。

```text
python -m pip install -r requirements-build.txt
python scripts/build_pdf.py
```

脚本读取正文、答案、附录和 SOURCES.md，生成 PDF、页码索引和原创 SVG 图示。字体缺失时构建会明确失败；应安装获授权字体或调整脚本中的字体路径，不能把缺字 PDF 当作成品。

## EPUB

EPUB 脚本只依赖 Python 标准库；仓库已保存 SVG，因此可以单独构建 EPUB。

```text
python scripts/build_epub.py
```

PDF 固定页码与 EPUB 流式分页不同。两者读取同一份内容，EPUB 有章节导航、图示、表格、代码、封面与提示框。

## 静态检查

临时目录应位于源仓库以外或被忽略的目录中。以下示例把检查文件放到相邻的 book-check-work。

```text
python scripts/verify_book.py --work-dir ../book-check-work
python scripts/verify_book.py --work-dir ../book-check-work --bash /bin/bash
```

Windows 如需 Git Bash，将 /bin/bash 替换成自己的 bash.exe 路径。脚本只对章节代码做 bash -n，不执行其中的命令。健康检查脚本使用模拟 curl 与 sleep，覆盖正常、异常正文、错误版本、重定向、连接失败和缺少参数，不启动服务。

不带 --bash 只运行源稿、示例一致性和 EPUB 结构检查，结果会如实记为本次没有做 Bash 检查。不要用一次较少检查的结果覆盖原有记录后仍声称所有检查通过。

## 版面验证

```text
pdftoppm -r 120 -png downloads/v0.2.1/Hola-Euler-v0.2.1.pdf ../book-check-work/page
```

检查整本页面，并放大新图示、长代码、提示框和表格。结构检查无法判断文字重叠或图形箭头含义。EPUB 结构检查也不能代表所有阅读器的兼容性，发布前还应在实际阅读器中打开。

## 历史版本

v0.1-review 保留初始源稿标签，v0.1.0 保存首轮 PDF、EPUB 与首页的归档提交。v0.2.0 对应静态审阅修订，v0.2.1 对应实机修订。历史下载文件不随当前正文重新生成，以免失去对照基线。
