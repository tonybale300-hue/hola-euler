# 第 17 章 管道与重定向

## 17.1 屏幕上的两种文字

### 17.1.1 为输入输出编号

程序可能打印正常结果，也可能打印错误说明。系统用文件描述符识别进程打开的输入输出对象，它是进程内的一个小整数编号。惯例中 0 是标准输入 stdin，1 是标准输出 stdout，2 是标准错误 stderr。它们常连接到终端，也可以改接文件或管道。

:::diagram streams

### 17.1.2 把正常结果保存到文件

```bash
mkdir -p ~/linux-lab/streams
cd ~/linux-lab/streams
printf '%s\n' first > result.txt
printf '%s\n' second >> result.txt
cat result.txt
```

符号 > 把标准输出指向文件，通常会创建文件或截断已有内容；>> 追加。两次执行后应看到 first 和 second 两行。重定向由 Shell 在启动命令前安排，因此 sort data.txt > data.txt 可能先截断输入。正确做法是输出到另一个文件，检查成功后再明确替换。

## 17.2 把错误单独保留

### 17.2.1 一个命令同时有成功和失败对象

```bash
ls result.txt missing.txt > out.txt 2> err.txt
cat out.txt
cat err.txt
```

假定 missing.txt 不存在，out.txt 保存正常列出的名称，err.txt 保存错误诊断。2> 明确指定标准错误描述符。看到屏幕安静不代表命令成功，消息可能都进入文件。命令退出状态仍需要检查，第 19 章会继续使用。

### 17.2.2 重定向从左到右处理

```bash
ls result.txt missing.txt > combined.txt 2>&1
```

先把 1 指到 combined.txt，再把 2 复制为当前 1 的目标，所以二者都进入同一个文件。若交换次序，2 先复制了原来的终端目标，再把 1 改到文件，错误仍可能留在终端。2>&1 中的 & 表示复制描述符目标，与后台运行的 & 语境不同。[S03b]

## 17.3 让一个程序的输出成为另一个的输入

### 17.3.1 管道连接的是流

```bash
printf '%s\n' pear apple pear | sort | uniq -c
```

| 把前一个命令的标准输出连接到下一个的标准输入。第一个产生三行，第二个排序，第三个统计相邻重复。普通管道不自动包含 stderr。参与管道的程序可以并发读写，不能理解为先把整个文件写完再启动下一个程序。

:::diagram pipeline

### 17.3.2 保存一份同时继续传递

```bash
printf '%s\n' alpha beta | tee captured.txt | wc -l
```

tee 的名字来自 T 形分流的形象，既把输入写到文件，也继续写到标准输出。此例 captured.txt 保留两行，末尾 wc -l 统计换行数。tee 默认会覆盖文件，-a 用于追加。知道权限由哪个进程使用，就能理解 sudo command > /etc/file 为何可能仍被拒绝，> 是普通 Shell 先处理的。需要管理员写配置时，后面的章节使用 sudo install 或经过检查的 sudo tee。

## 17.4 多行输入与退出状态

### 17.4.1 here-document 让模板易读

```bash
cat > example.conf <<'EOF'
name=linux-lab
path=$HOME
EOF
```

<< 引入 here-document，把后续多行作为输入直到结束标记。'EOF' 的引号让正文不做变量等展开，因此文件中保留字面 $HOME。结束标记要独占一行。此方法后面用于写配置，写之前仍要检查是否会覆盖同名文件。

### 17.4.2 管道最后一段成功不代表前面都成功

Bash 默认用管道最后一条命令的退出状态作为整个管道的状态。set -o pipefail 可以让前面失败更容易暴露，但它也要求理解各工具的退出规则，例如没有匹配的 grep 返回 1。脚本不应只加一个选项就停止判断错误，第 19 章给出显式判断。

## 17.5 本章练习

- 不要往前翻｜0、1、2 分别是什么？
- 命令填空｜只把错误写入 err.txt 使用 ______ err.txt。
- 看需求写命令｜把一次 ls 的正常与错误输出一起保存。
- 看命令猜结果｜cmd 2>&1 >file 与 cmd >file 2>&1 是否相同？
- 找错误｜cat note.txt > note.txt 为什么不能当作“原样保存”？
- 无提示实操｜用自己创建的文件触发一条可控错误，分别保存两种输出，再组成一条排序统计管道。

本章新命令为 tee / T 形分流；set 是设置 Shell 选项的内建命令。复用 printf、ls、sort、uniq、wc、cat。明天先画出描述符去向，再写命令。

资料依据见 S03a、S03b、S04。答案见第 17 章答案。
