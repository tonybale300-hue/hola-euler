# 第 20 章 Shell Script 实战

> 本章任务｜完成一次备份恢复，验证健康检查能够识别异常。

## 20.1 为自己的笔记生成可恢复归档

### 20.1.1 先定义输入、输出与失败条件

本章备份范围固定为 ~/linux-lab/notes，输出位于 ~/linux-lab/backups 的独立目录。脚本不删除旧备份，不接收任意系统路径。每次成功应生成一份压缩归档及一个 SHA256 文件。如果源目录不存在、打包失败或校验失败，就返回非零状态，保留现场供检查。

```bash
mkdir -p ~/linux-lab/notes ~/linux-lab/scripts
printf '%s\n' 'Linux practice' > ~/linux-lab/notes/day1.txt
```

### 20.1.2 把脚本保存为 backup-notes.sh

```bash
#!/usr/bin/env bash
set -u
umask 077
root="$HOME/linux-lab"
source_dir="$root/notes"
backup_root="$root/backups"
if [ ! -d "$source_dir" ]; then
  printf 'Missing directory: %s\n' "$source_dir" >&2
  exit 1
fi
if ! mkdir -p -- "$backup_root"; then
  exit 1
fi
run_dir=$(mktemp -d "$backup_root/run.XXXXXXXX") || exit 1
archive="$run_dir/notes.tar.gz"
if ! tar -czf "$archive" -C "$source_dir" .; then
  printf 'Archive failed; inspect %s\n' "$run_dir" >&2
  exit 1
fi
if ! (
  cd "$run_dir" || exit 1
  sha256sum notes.tar.gz > notes.tar.gz.sha256 &&
    sha256sum -c notes.tar.gz.sha256
); then
  printf 'Checksum failed: %s\n' "$run_dir" >&2
  exit 1
fi
printf 'Backup ready: %s\n' "$run_dir"
```

mktemp 关联 make temporary，-d 创建唯一目录，XXXXXXXX 是随机名称模板。独立目录避免重复运行直接覆盖同名归档。umask 077 让新建内容默认更私有。set -u 让未设置变量的展开更容易暴露，但不能替代检查变量值是否符合业务要求。

圆括号创建子 Shell，其中的 cd 不会改变脚本其余部分的工作目录。&& 只在前一步成功时继续。摘要文件写入相对文件名，便于把整份备份目录一起搬到其他位置验证。

## 20.2 检验脚本是否真的可靠

### 20.2.1 三类测试

```bash
cd ~/linux-lab/scripts
bash -n backup-notes.sh
bash backup-notes.sh
```

正常运行后不要只读“Backup ready”。找到输出目录，列出归档清单，在新目录恢复并比较内容。再暂时把 notes 改名，验证脚本明确失败且不报告成功，随后恢复名称。最后在 notes 中放入含空格文件名，确认归档仍保留完整名字。每次失败都要记录退出状态与诊断位置。

### 20.2.2 这份脚本的边界

这是个人实验目录的归档脚本。它假设目录由当前用户控制，不为多个不可信用户共享写入的环境设计，也不保证备份期间不断变化的文件具有应用一致性。未来加入数据库、自动清理和定时执行时，需要分别设计一致性、保留策略与并发控制。

## 20.3 为应用写一个小型健康检查

### 20.3.1 只检查明确的接口

第 22 章的应用提供 /health。保存下面脚本为 check-health.sh，在应用启动后运行。

```bash
#!/usr/bin/env bash
url='http://127.0.0.1:8080/health'
if ! body=$(curl -fsS --noproxy '*' \
    --connect-timeout 2 --max-time 5 \
    --write-out '\n%{http_code}' "$url"); then
  printf 'Request failed: %s\n' "$url" >&2
  exit 1
fi
if [ "$body" != $'ok\n\n200' ]; then
  printf 'Unexpected response: %s\n' "$body" >&2
  exit 1
fi
printf '%s\n' 'healthy'
```

curl 的 -f 对 HTTP 错误状态返回失败，-s 减少进度信息，-S 在静默模式下仍显示错误。--max-time 限制总耗时，避免请求无限等待。--noproxy 指定本机请求不走代理，--write-out 在正文后追加状态码。$(...) 捕获输出并去掉末尾换行。本例正文约定为 ok 加一个换行，再接输出格式中的换行和 200，因此比较值写成 $'ok\n\n200'。这个 Bash 语法把 \n 转成真正换行，同时核对状态和正文，拒绝携带 ok 文字的重定向响应。HTTP 成功也不必然等于业务健康，检查内容应与应用约定一致。

### 20.3.2 故障时只提供证据

检查失败后，查看 systemctl status、journalctl 和 ss。不要自动无限重启服务，这可能掩盖根因，甚至反复中断仍可处理的请求。自动修复应在人工理解失败原因之后再设计。

## 20.4 本章练习

- 不要往前翻｜为什么每次备份生成一个新目录？
- 命令填空｜限制 curl 总执行时间使用 ______ 5。
- 看需求写命令｜先检查 backup-notes.sh 语法，再运行。
- 看命令猜结果｜健康接口返回 HTTP 200、正文 failed，本章脚本会成功吗？
- 找错误｜只在 tar 后打印 done，却不检查 tar 结果，会造成什么误判？
- 无提示实操｜完成一次成功备份与一次源目录缺失测试，恢复源目录后，独立验证归档可恢复。

本章新命令为 mktemp / make temporary，新增 !、&&、$(...) 与子 Shell 的组合。十分钟后解释每一个 exit 1 对应的失败原因，一周后实际恢复一次备份。

资料依据见 S03、S04、S13、S15。答案见第 20 章答案。完整脚本随 examples/ 一起提供。
