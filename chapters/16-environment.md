# 第 16 章 Bash 环境与环境变量

## 16.1 同样的命令为什么在另一个终端不一样

### 16.1.1 变量先属于当前 Shell

```bash
lab_message='hello environment'
printf '%s\n' "$lab_message"
bash -c 'printf "%s\n" "${lab_message-unset}"'
```

变量为一个名称保存值。赋值时等号两边不留空格，展开时加 $。双引号允许变量展开，并保留值里的空格。第三行启动另一个 Bash，-c 指定要执行的命令文本。${lab_message-unset} 表示变量未设置时用 unset 这个文字。这里子 Bash 默认看不到尚未导出的 lab_message。

### 16.1.2 export 把值传给后来的子进程

```bash
export lab_message
bash -c 'printf "%s\n" "$lab_message"'
unset lab_message
```

export 是导出，把变量加入随后启动程序可继承的环境。unset 取消设置。环境变量是每个进程环境的一部分，子进程改自己的环境不会倒过来修改父 Shell，也不会让其他已有终端同步更新。敏感变量不适合随意打印到日志或故障截图中。

## 16.2 PATH 怎样找到程序

### 16.2.1 按目录顺序查找

```bash
printf '%s\n' "$PATH"
type java
command -v bash
```

PATH 保存一组用冒号分隔的目录。Bash 对外部命令进行路径查找时会使用它。command -v 查询命令怎样被解析，可用于脚本判断可用性。command 是 Bash 内建工具，不需要把名字编成缩写。

:::diagram pathlookup

如果当前目录有 report.sh，直接输入 report.sh 不一定能找到，因为当前目录通常不在 PATH 中。使用 ./report.sh 明确指出路径。不要把 . 放到 PATH 开头，那会让工作目录里同名程序优先于可信系统工具。

### 16.2.2 临时设置比全局修改更容易检查

```bash
LC_ALL=C sort ~/linux-lab/text/fruit.txt
```

这只为一次命令设置区域相关环境，便于得到稳定的字节排序。命令结束后当前 Shell 的长期设置不因此改变。相比直接修改 /etc 中的全局环境文件，这种局部设置更适合实验。

## 16.3 启动文件何时读取

### 16.3.1 交互与登录是两个维度

Bash 的启动文件取决于启动方式。交互式非登录 Bash 通常读取 ~/.bashrc；登录 Bash 读取 /etc/profile，再按规则选择用户的登录初始化文件。发行版可能通过某个文件继续加载另一个文件。非交互脚本的规则又不同，因此“我写进 .bashrc，所有服务都会得到它”并不成立。

systemd 服务通常不启动登录 Shell，不会自动继承你终端里的 export 和别名。服务应在自己的配置中声明必要环境，并在 ExecStart 使用经过验证的程序路径。

### 16.3.2 source 会在当前 Shell 中执行

source 文件路径让 Bash 在当前进程中执行文件内容；点命令 . 也有相关用法。只有确认文件内容可信时才执行，不能把它当成纯粹“读取文本”。一个写错的 source 文件可以改变当前目录、变量和函数，甚至执行其他操作。编辑初始化文件前先复制备份，再另开终端验证，保留当前可用会话。

## 16.4 本章练习

- 不要往前翻｜普通变量与导出变量的差异在哪里？
- 命令填空｜让后续子进程继承变量使用 ______ lab_message。
- 看需求写命令｜设置带空格的变量并完整输出。
- 看命令猜结果｜子 Bash 执行 unset，会自动移除父 Shell 的同名变量吗？
- 找错误｜PATH="." 为何可能使常用命令找不到，并引入执行错误程序的风险？
- 无提示实操｜用父、子两个 Bash 证明 export 的作用，结束后清理自己创建的变量。

本章新命令为 export / 导出、unset / 取消设置、command / 命令查询与执行控制、source / 在当前环境执行文件。复用 type 和 printf，三天后解释服务为什么看不到终端变量。

资料依据见 S03、S09。答案见第 16 章答案。
