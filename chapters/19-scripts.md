# 第 19 章 Shell Script 入门

> 本章任务｜写一份有参数检查的脚本，解释失败时的退出状态。

## 19.1 把重复步骤写进一个文件

### 19.1.1 第一份脚本

Shell Script 是由 Shell 解释执行的一组命令。脚本能保留操作步骤，但同样会重复其中的错误，所以先从只读任务开始。

```bash
mkdir -p ~/linux-lab/scripts
cd ~/linux-lab/scripts
vim hello.sh
```

把下一段保存为 hello.sh 的文件内容，保存后退出编辑器。含有 #!/usr/bin/env bash 的代码块是完整脚本内容，不能直接粘贴到交互终端，尤其不要在自己的登录 Shell 中试执行其中的 exit。

```bash
#!/usr/bin/env bash
name=${1:-reader}
printf 'Hello, %s\n' "$name"
printf 'Current directory: %s\n' "$PWD"
```

首行叫 shebang，提示按哪个解释器启动。/usr/bin/env bash 通过环境中的 PATH 找 Bash。env 就是 environment 工具。对系统服务等强调固定环境的场景，应使用验证过的绝对解释器路径。${1:-reader} 使用第一个位置参数，未设置或为空时用 reader。

```bash
bash -n hello.sh
bash hello.sh Alex
chmod u+x hello.sh
./hello.sh Alex
```

bash -n 只做语法检查，不执行命令；它不能证明路径、权限和业务逻辑正确。用 bash hello.sh 不要求脚本有执行位，但必须可读。./hello.sh 是直接执行路径，需要相应执行权限和有效解释器。

## 19.2 成功与失败需要明确判断

### 19.2.1 退出状态

每条命令结束时提供退出状态，通常 0 表示成功，非 0 表示其他情况，具体含义依工具而定。$? 保存最近一个前台命令或管道的退出状态，下一条命令会覆盖它。尽量直接把要判断的命令放在 if 后，减少检查错对象的机会。

```bash
if test -r "$1"; then
  printf 'Readable: %s\n' "$1"
else
  printf 'Cannot read: %s\n' "$1" >&2
  exit 1
fi
```

test 的普通词义是测试，-r 检查当前身份是否可读。then 后面是条件成立分支，else 是另一分支，fi 结束 if。实际脚本应先检查参数数量，避免没有参数时继续操作；下一节会补上。退出状态只有程序自己定义的一层信息，仍应配合日志。

### 19.2.2 参数校验写在操作之前

```bash
#!/usr/bin/env bash
if [ "$#" -ne 1 ]; then
  printf 'Usage: %s FILE\n' "$0" >&2
  exit 2
fi
if [ ! -f "$1" ]; then
  printf 'Not a regular file: %s\n' "$1" >&2
  exit 1
fi
wc -l -- "$1"
```

$# 是参数个数，$0 是脚本调用名称，$1 是首个参数。[ 是 test 的一种形式，前后空格和最后的 ] 都是语法所需。-ne 是数值不等于，-f 检查普通文件，! 取反。-- 表示后面的参数不再作为选项解析，防止文件名以 - 开头时被误读。

## 19.3 循环与函数

### 19.3.1 保留每个参数的完整边界

```bash
for file in "$@"; do
  if [ -f "$file" ]; then
    wc -l -- "$file"
  fi
done
```

"$@" 将每个位置参数保持为独立对象，含空格的名字不会被再次拆分。for 逐个取值，do 与 done 包住动作。不要用 for file in $(ls) 遍历文件，那会把输出文本重新按空白拆开。

### 19.3.2 函数只组合清楚的工作

```bash
show_file() {
  local file=$1
  printf 'File: %s\n' "$file"
  wc -l -- "$file"
}
```

函数把重复动作封装起来，local 限制变量在当前函数的局部范围。函数参数与脚本位置参数规则类似。起步时让一个函数完成一个可描述的小任务，不要把提权、网络下载和文件删除混进一个“万能函数”。

## 19.4 调试与执行边界

脚本出现语法错误，先用 bash -n；逻辑不对时可以用 bash -x 跟踪实际执行，但跟踪可能显示变量展开后的秘密内容。Windows 编辑的 CRLF 行尾有时让解释器看到额外的回车，脚本应保存为 UTF-8 与 LF 换行。set -e 有复杂例外，不应代替关键步骤的显式判断；本书第 20 章保留清楚的失败分支。

## 19.5 本章练习

- 不要往前翻｜直接执行脚本与 bash script.sh 有什么区别？
- 命令填空｜检查语法但不执行使用 bash ______ script.sh。
- 看需求写命令｜把首个参数保存到变量并完整输出。
- 看命令猜结果｜传入 'my notes.txt' 时，"$@" 保留几个参数？
- 找错误｜name = Alex 为什么不能按变量赋值理解？
- 无提示实操｜写一个只接受一个文件参数的行数脚本，测试无参数、不存在文件和含空格文件名三种情况。

本章新语法为 if、for、函数和位置参数；新命令或内建为 test、[、exit、local、env。复用 chmod、wc、printf。明天先写错误分支，再补正常分支。

资料依据见 S03、S04。答案见第 19 章答案。
