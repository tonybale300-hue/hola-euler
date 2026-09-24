# 第 14 章 压缩、打包与归档

> 本章任务｜打包、校验、恢复自己的文件，并比较恢复内容。

## 14.1 把多个文件装进一个文件

### 14.1.1 归档与压缩分开看

传输一整组文件时，逐个复制容易漏掉目录结构。归档把多个文件与元数据组织成一个文件，压缩则用更紧凑的编码减少体积。tar 的名字来自 tape archive，最初与磁带归档有关，现在常用于普通文件。gzip 关联 GNU zip，一般压缩一个数据流。tar.gz 通常表示先归档再 gzip 压缩。

```bash
mkdir -p ~/linux-lab/archive/source
cd ~/linux-lab/archive
printf '%s\n' 'alpha' > source/a.txt
printf '%s\n' 'beta' > source/b.txt
tar -czf notes.tar.gz -C source .
tar -tzf notes.tar.gz
```

c 是 create，新建归档；z 使用 gzip；f 指定归档文件名。-C source 要求 tar 先切换到 source，再处理后面的 .。这样包内名称相对于 source，不会把整段家目录路径打进去。t 是 list，查看目录清单，不执行解包。

## 14.2 恢复要在新目录中演练

### 14.2.1 看过清单再解开

```bash
mkdir restore
tar -xzf notes.tar.gz -C restore
ls -l restore
cmp source/a.txt restore/a.txt
```

x 是 extract，提取。-C restore 指定已有的解包目录。cmp 关联 compare，逐字节比较两个文件，相同通常不输出文字并成功退出。这里比较一份样本，在真实备份中还要检查完整文件清单、权限、必要元数据以及应用能否使用恢复后的文件。

对陌生归档，应先列出内容，在隔离的新目录、普通用户身份下检查。归档中可能有意外路径、链接或覆盖目标，不能直接用 root 解到 /etc 或根目录。不要把“tar 有某些路径保护”理解成允许任意信任来源。

### 14.2.2 文件存在不等于备份可靠

把归档保存在同一块磁盘上，原盘故障时仍可能一起丢失。可用的备份至少要有清楚的内容范围、独立保存位置和恢复验证。运行中的数据库与不断变化的文件可能需要专门的一致性备份流程，仅用 tar 不能保证一致状态。

## 14.3 校验内容变化

### 14.3.1 为归档生成摘要

```bash
sha256sum notes.tar.gz > notes.tar.gz.sha256
sha256sum -c notes.tar.gz.sha256
```

sha256sum 计算 SHA-256 摘要，-c 按校验文件验证。摘要改变说明字节内容不同，可能来自传输损坏或后续修改。若攻击者能同时替换归档与摘要，这种比较不能单独证明发布者身份，需要可信的签名或传递途径。

### 14.3.2 命令写反会改变任务

tar -czf backup.tar.gz source 创建，tar -xzf backup.tar.gz 提取。同样的几个字母组合，一位不同就会执行不同动作。先口头读出“我要创建”“我要列出”还是“我要恢复”，再决定 c、t、x，能比死背一整条命令更稳。

## 14.4 本章练习

- 不要往前翻｜归档和压缩各负责什么？
- 命令填空｜只看压缩归档清单使用 tar -______ notes.tar.gz。
- 看需求写命令｜把 source 内的内容归档，并恢复到新的 restore2 目录。
- 看命令猜结果｜tar -C source . 中的 . 指向执行命令前的目录吗？
- 找错误｜备份只验证“文件有 1 MB”，缺少哪些检查？
- 无提示实操｜归档自己的一个实验目录，生成摘要，在新目录恢复，比较文件内容，写出恢复步骤。

本章新命令为 tar / tape archive、gzip / GNU zip、cmp / compare、sha256sum / SHA-256 checksum。复用 cp 和权限知识，七天后不看原命令做一次恢复。

资料依据见 S15、S04。答案见第 14 章答案。
