# 第 5 章 查看与处理文本

## 5.1 文件有内容以后怎样阅读

### 5.1.1 准备一份小日志

日志是程序按时间或事件写出的记录。我们先手工制造一份教学数据，练习查看方法，不把它当作某个真实服务的运行记录。

```bash
mkdir -p ~/linux-lab/text
cd ~/linux-lab/text
printf '%s\n' 'INFO start' 'INFO ready' 'WARN slow' \
  'ERROR timeout' 'INFO stop' > app.log
cat app.log
```

行尾的反斜杠表示这条命令在下一物理行继续，反斜杠后面不要再加空格。printf 按格式输出五个参数，> 把内容保存到 app.log。这份文件较短，可以用 cat 一次读完。文件很大时，连续滚屏很难定位，这时换成分页阅读。

### 5.1.2 less 让阅读可以停下来

```bash
less app.log
```

less 是分页器，其名字与早期 more 分页工具有联系；这里把它记成可以前后移动的阅读工具即可。按上下方向键移动，空格向后翻一屏，b 向前翻一屏，/ERROR 搜索 ERROR，n 找下一个匹配，q 退出。阅读工具一般不修改文件，退出后文件仍保持原样。最小安装若没有 less，先用 cat，包管理方法见第 9 章。

## 5.2 只看需要的几行

### 5.2.1 头部和尾部

```bash
head -n 2 app.log
tail -n 2 app.log
wc -l app.log
```

head 和 tail 分别是头部、尾部的英文词。-n 2 指定两行。第一条应选出前两行，第二条应选出最后两行。wc 来源可与 word count 关联，-l 统计换行符数量；本例每行都以换行结束，所以结果为五。如果文件最后一段没有换行，肉眼看到的行数可能与 wc -l 不同。

### 5.2.2 跟随追加内容

在终端 A 中运行 tail -f app.log，-f 表示 follow，等待文件的新内容。在终端 B 中进入同一目录，运行下面一行。

```bash
printf '%s\n' 'INFO another event' >> app.log
```

>> 追加而不清空旧内容。回到终端 A 应能看见新增行。按 Ctrl+C 结束跟随，并不删除日志。如果程序会把旧日志改名后新建同名文件，GNU tail 的 -F 还能结合按名称跟随与重试；普通 -f 与 -F 在日志轮转时的差异应结合实际程序验证。

## 5.3 把重复内容整理出来

### 5.3.1 顺序决定去重结果

```bash
printf '%s\n' pear apple pear apple > fruit.txt
sort fruit.txt
sort fruit.txt > sorted.txt
uniq -c sorted.txt
```

sort 就是排序，默认按当前区域设置的排序规则处理整行。它把结果写到标准输出，不会自动修改源文件。uniq 与 unique 关联，只合并相邻重复行；-c 显示相邻组的出现次数。因此我们先排序，再用 uniq。输出中的顺序可能随区域设置变化，若实验要求固定字节顺序，可在命令前写 LC_ALL=C。

### 5.3.2 切出简单字段

```bash
printf '%s\n' 'alex:student' 'sam:teacher' > roles.txt
cut -d ':' -f 1 roles.txt
```

cut 的意思是切取，-d 指定分隔符，-f 1 选择第一字段。这里每行用一个冒号分开名称和角色。预期输出 alex 与 sam。复杂 CSV 可能含引号和字段内逗号，不能直接把 cut -d ',' 当作完整 CSV 解析器。

## 5.4 本章练习

- 不要往前翻｜cat 与 less 适合怎样的阅读场景？
- 命令填空｜读取最后三行使用 tail ______ 3 app.log。
- 看需求写命令｜查看日志前两行并统计换行符数量。
- 看命令猜结果｜fruit.txt 未排序直接交给 uniq，隔行重复的 pear 会全部合并吗？
- 找错误｜sort fruit.txt > fruit.txt 为什么可能把输入清空？先保留这个问题，到第 17 章再解释打开文件的时机。
- 无提示实操｜建立一份六行名单，把排序结果保存为新文件，统计每个相邻重复组的数量，保留原始文件。

本章新命令为 less / 分页器名称、head / 头、tail / 尾、wc / word count、sort / 排序、uniq / unique、cut / 切取。复习时仍使用第 4 章的 cp，先保留数据副本。

资料依据见 S04、S03。答案见第 5 章答案。
