# 第 7 章 用户与用户组

## 7.1 程序究竟以谁的身份运行

### 7.1.1 看看当前账户

```bash
whoami
id
```

whoami 连起来就是 who am I，显示当前有效用户名称。id 是 identity 的词义关联，用数字与名称展示用户及所属组。UID 是 user identifier，用户标识；GID 是 group identifier，组标识。名字方便人阅读，系统在许多权限判断中使用数字。

一个用户通常有一个主组，还可以属于多个附加组。组为多个账户共享权限提供一种组织方式。把人加入一个组，并不会自动让所有文件对这个组开放，文件的所属组与权限仍需配合。

:::diagram users

### 7.1.2 查询账户数据库

```bash
getent passwd "$USER"
getent group
```

getent 可理解为 get entries，按系统配置查询名称服务数据库条目。passwd 在这里是数据库名，不是在改密码。$USER 是变量展开，此处先知道它通常记录登录用户名；有效身份以 id 为准。passwd 条目通常包含用户名、密码占位符、UID、GID、说明、家目录和登录 Shell，字段以冒号分隔。密码散列通常放在受保护的 /etc/shadow 中，不应复制到学习笔记。

## 7.2 临时管理权限与切换身份

### 7.2.1 sudo 的范围

```bash
sudo -l
```

sudo 可以理解为以指定用户执行命令的工具，默认目标通常是 root。名称历史常与 superuser do 关联，但实际能力包含其他目标用户，因此本书不把它解释成只能“变成 root”。-l 列出当前策略允许的操作，可能要求输入当前用户自己的密码。

su 表示 substitute user，切换用户身份；su - 使用接近登录的环境。默认目标是 root，认证要求取决于策略，通常涉及目标账户密码。sudo 与 su 的授权机制和环境行为不同，不能只按“都能提权”互换。

### 7.2.2 没有授权时怎样继续

若普通用户不在 sudo 授权范围内，先使用虚拟机控制台与安装时建立的管理员入口。由已授权管理员检查本机策略，必要时通过 visudo 修改，visudo 会在保存时检查语法。不要直接向 /etc/sudoers 随意追加文本。把用户加入 wheel 是否获得 sudo 权限取决于启用的策略，不能只凭组名断言。

> 实机核验｜【待 openEuler 24.03 LTS SP4 实机验证】应保存目标安装中 sudo、wheel 与管理员账户的实际策略。后文带 sudo 的实验以已经建立合法管理权限为前提。

## 7.3 创建一个可辨认的练习账户

### 7.3.1 先检查名称，再创建

只在自己的专用虚拟机中完成本节。labreader 是本书练习名，若已存在就改用另一个未使用的名字，并在后续命令保持一致。

```bash
getent passwd labreader
sudo useradd -m labreader
id labreader
```

第一条如果已有输出，停止创建并检查现有账户用途。useradd 由 user 与 add 组成，创建用户；-m 要求创建家目录。没有给该账户设置登录密码，因此不要把“账户创建成功”理解成“可以立即密码登录”。登录策略还受锁定状态与 Shell 等条件影响。

### 7.3.2 附加组不能误覆盖

groupadd 用于新增组，usermod 用于修改账户。下面创建练习组并把 labreader 追加进去，同样先确认名称未被使用。

```bash
getent group labteam
sudo groupadd labteam
sudo usermod -aG labteam labreader
id labreader
```

-G 设置附加组列表，-a 表示 append，追加。遗漏 -a 可能把其他附加组从列表中移除。组关系变化后，已有进程不会自动全部获得新组身份，通常需要新登录会话。实验结束后可以保留账户用于第 8 章观察，无须急着删除家目录。

## 7.4 本章练习

- 不要往前翻｜主组与附加组有什么用途？
- 命令填空｜查看自己的 UID 和组列表使用 ______。
- 看需求写命令｜查询 labreader 的账户条目与组归属。
- 看命令猜结果｜usermod -G team 用户名 与加上 -a 后的操作有什么差异？
- 找错误｜“加入 wheel 就一定能用 sudo”，遗漏了什么条件？
- 无提示实操｜在记录中列出普通用户、管理员、专用服务用户各需要怎样的权限，暂不创建服务用户，留给第 24 章。

本章新命令为 whoami / who am I、id / identity、getent / get entries、sudo / 按策略换身份执行、su / substitute user、useradd / add user、groupadd / add group、usermod / modify user、visudo / 安全编辑 sudo 策略。名称关联服务于理解，不代表所有名称都有一个唯一正式英文全称。

资料依据见 S06、S12。答案见第 7 章答案。
