# v0.2.0 全书命令审查

审查日期为 2026-09-23 至 2026-09-24。范围包括第 0 至 24 章的命令块、正文内命令、150 道练习与答案、5 个附录，以及 8 份可下载示例。静态审查检查语义、参数、前置文件、执行位置、用户身份和失败后的行为，不能证明所有命令已经在 openEuler 执行成功。

## 发现与修订

| 编号 | 位置 | 问题 | 本次处理 |
|---|---|---|---|
| R01 | 第 4 章练习 | 练习引用前面已删除的 hello.txt | 改用 original.txt，答案同步补执行目录和重新准备条件 |
| R02 | 第 7 章 | USER 环境变量不保证代表有效身份 | 改用 id -un 的查询结果，并解释变量与实际身份的差异 |
| R03 | 第 8 章 | root 下观察权限可能得到误导结果 | 补普通用户验证提示 |
| R04 | 第 9 章 | 查询权限和非零退出状态容易混淆 | 明确普通查询与安装权限，补 check-update 的 0、100、1 区分 |
| R05 | 第 12 章 | 只限制连接阶段，HTTP 请求仍可能长时间等待 | 加 --max-time 15，并解释与连接超时的差别 |
| R06 | 第 13 章 | 自定义密钥路径的父目录可能尚不存在 | 补建目录步骤与 Windows 客户端说明 |
| R07 | 第 13 章 | 隧道监听失败可能只输出提示，初学者误以为可用 | 加 ExitOnForwardFailure=yes，说明不能据此保证后端可达 |
| R08 | 第 16 章 | PATH 实验查询尚未要求安装的 Java | 改查已经使用的 Bash |
| R09 | 第 19 章 | 脚本文件内容与交互命令容易被混贴 | 补目录和编辑命令，明确 exit 所在脚本不能当作整章交互命令执行 |
| R10 | 第 20 章 | 健康检查只比正文，没有明确验证 HTTP 200 | 同时检查状态与正文，绕过本机请求的代理；增加失败分支模拟检查 |
| R11 | 第 22 章 | Java 和 Spring 目录只在叙述中提及，Maven 当前目录不明确 | 补完整 mkdir、cd 与源码目录，Maven 构建前显式切换目录 |
| R12 | 第 22 章 Java | 405 缺 Allow；HEAD 请求不应发送响应正文 | 补 Allow，并对 HEAD 使用无正文响应；重新编译通过，运行尚待验证 |
| R13 | 第 24 章 | 部署配置目录缺具体创建步骤 | 补 mkdir、cd、vim 操作 |
| R14 | 第 24 章 | ln 遇到指向目录的既有目标可能进入该目录 | 使用 ln -sT，并要求目标不存在 |
| R15 | 第 24 章 | 连续切换命令在中途失败后仍可能继续执行 | 增加目标和悬空链接检查，用 && 串联关键步骤，说明失败后保留现场 |
| R16 | 第 24 章 | Type=simple 返回不代表应用已经就绪 | 增加有限重试脚本，同时检查 HTTP 200 与预期版本 |
| R17 | 源文件展示 | 自定义图示标记不能直接在 GitHub Markdown 中显示 | 改为标准 Markdown 图片链接，PDF、EPUB 仍使用同一套图示 |

## 逐章复核记录

| 章节 | 核对的主要命令或语义 | 结论与仍需实机检查的部分 |
|---|---|---|
| 0 | mkdir -p、cd、pwd、命令格式与提示符 | 基本语义一致；补逐行执行与预计失败的说明 |
| 1 | os-release、uname、安装与身份 | 发行版和内核区分正确；安装器与镜像验收待执行 |
| 2 | printf、type、help、man、pwdd | pwdd 是故意的失败示例；man 和分页器可用性依安装结果 |
| 3 | 相对路径、引号、失败 cd | 路径依赖明确；重复练习时已有目录产生报错属正常条件差异 |
| 4 | touch、cp、mv、rm、rmdir、ln | 修订 R01；复制已有目录与硬链接关系已核对 |
| 5 | cat、less、head、tail、wc、sort、uniq、cut | 以换行计数、相邻去重的解释正确；教学日志保留原文件 |
| 6 | Vim 模式、保存、撤销、替换 | 键序列在 Vim 中执行；新增模式图 |
| 7 | whoami、id、getent、sudo、useradd、usermod | 修订 R02；账户名占用检查和 sudo 策略仍要实机核对 |
| 8 | chmod、目录权限、chown、umask | 修订 R03；ACL、挂载与安全策略明确在基础权限之外 |
| 9 | DNF 查询安装、rpm -q/-ql/-qf | 修订 R04；候选包、仓库与实际安装交易待验证 |
| 10 | 后台任务、PID、ps、kill、jobs | 仅操作当前实验创建的进程；作业表与 PID 未混同 |
| 11 | systemctl、journalctl、unit、ExecStart | 启用与活动状态、daemon-reload 与重启的区别正确；目标单元待核对 |
| 12 | ip、nmcli、getent、ping、ss、curl | 修订 R05；连接名和设备名依本机查询，不套固定网关 |
| 13 | ssh-keygen、ssh-copy-id、scp、ssh -L | 修订 R06/R07；认证、指纹和双端转发仍需真实连接 |
| 14 | tar -c/-t/-x/-C、cmp、sha256sum | 创建与恢复对象不同；摘要不单独证明来源，恢复应另测 |
| 15 | lsblk、findmnt、df、du、mount、umount | 不含真实盘格式化指令；tmpfs 挂载权限和卸载待虚拟机执行 |
| 16 | export、unset、PATH、command、source | 修订 R08；父子环境与启动文件条件已核对 |
| 17 | 标准描述符、管道、tee、here-document | 重定向次序与 quoted delimiter 正确；新增次序对比图 |
| 18 | grep -F/-E、find -name/-exec | 引号和含空格文件名传递正确；不把通配符当正则 |
| 19 | bash -n、参数、test、if、for、函数 | 修订 R09；中间片段有前提，完整脚本另有参数检查 |
| 20 | 归档失败、摘要、curl 健康检查 | 修订 R10；模拟成功、正文错误、重定向和连接失败，不代替真实网络 |
| 21 | Git 初始化、忽略、暂存、提交与差异 | 署名只改本地项目配置；没有把 init 说成远程发布 |
| 22 | JDK、javac、jar、Maven 与 Java 示例 | 修订 R11/R12；标准 Java 重编译通过，Maven 解析与运行待验证 |
| 23 | firewalld、SELinux、目录所有权、入口 | 只读查询与未来公网部署分开；不以关闭保护解决问题 |
| 24 | install、systemd、ln/mv、等待与回滚 | 修订 R13 至 R16；端到端部署和重启恢复尚未执行 |

参考答案与附录已随正文对照，包含故意失败的题目；这些题目中的错误命令不能收入“可直接执行”列表。

## 可复查的检查结果

[command-inventory.json](command-inventory.json) 为全部 114 个代码块记录章节、行号、语言与内容 SHA256，其中 103 个为 Bash。行号和摘要可用来识别后续版本是否改变了已审查代码。

[static-check-results.json](static-check-results.json) 保存本次自动检查结果。103 个 Bash 块通过 Git Bash 的 bash -n；8 份示例与正文相应代码一致。两个检查脚本的 9 个模拟用例通过，模拟中未连接任何真实服务器。

标准 Java 示例用 Windows 上已有 JDK 执行 javac --release 21 编译通过。本轮没有启动 Java 服务；旧版运行证据不能自动转成新版运行结论。Spring Boot 的 pom.xml 仅做 XML 结构检查，尚未执行 Maven 构建。

2026-09-24 已完成专用 SSH 密钥认证，确认虚拟机为 openEuler 24.03 LTS SP4 x86_64。只读清单核对了系统版本、工具与已安装包；103 段 Bash 示例在目标 Bash 5.2.15 下通过 bash -n，未执行示例正文。本次检查未安装软件、创建账户或修改服务、网络、防火墙与挂载。Vim、JDK、Maven 尚未安装，继续按 [VALIDATION.md](VALIDATION.md) 逐项实测，结果见 [vm-check-results.json](vm-check-results.json)。
