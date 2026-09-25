# 参考资料与版本核验

所有条目查询日期为 2026-09-23。优先使用官方项目材料。上游当前手册只用于确认基础语义，不能证明 openEuler 目标包包含所有新功能。书中实验、图示和叙述为本项目原创设计，未复制其他教材章节。

## S01 openEuler 官方下载与 SP4 镜像目录

对应章节 1、9、附录 D。适用范围为 24.03 LTS SP4。用途为 确认目标版本与架构；不是安装实测。

[https://www.openeuler.org/zh/download/](https://www.openeuler.org/zh/download/)

[https://repo.openeuler.org/openEuler-24.03-LTS-SP4/ISO/](https://repo.openeuler.org/openEuler-24.03-LTS-SP4/ISO/)

## S02 openEuler SP4 快速入门与系统信息

对应章节 1。适用范围为 24.03 LTS SP4。用途为 安装流程和版本查询；虚拟机配置为本书建议。

[https://docs.openeuler.org/en/docs/24.03_LTS_SP4/server/quickstart/quick_start_server.html](https://docs.openeuler.org/en/docs/24.03_LTS_SP4/server/quickstart/quick_start_server.html)

[https://docs.openeuler.org/en/docs/24.03_LTS_SP4/server/administration/administrator/viewing_system_information.html](https://docs.openeuler.org/en/docs/24.03_LTS_SP4/server/administration/administrator/viewing_system_information.html)

## S03 GNU Bash Reference Manual

对应章节 0、2、3、16 至 20。适用范围为 上游手册；SP4 自带版本待核对。用途为 Shell 语义、引号、变量、条件和参数。

[https://www.gnu.org/s/bash/manual/bash.html](https://www.gnu.org/s/bash/manual/bash.html)

## S03a Bash Pipelines

对应章节 17。适用范围为 上游稳定语义。用途为 管道连接与执行状态。

[https://www.gnu.org/s/bash/manual/html_node/Pipelines.html](https://www.gnu.org/s/bash/manual/html_node/Pipelines.html)

## S03b Bash Redirections

对应章节 17。适用范围为 上游稳定语义。用途为 描述符复制、打开文件与重定向次序。

[https://www.gnu.org/s/bash/manual/html_node/Redirections.html](https://www.gnu.org/s/bash/manual/html_node/Redirections.html)

## S04 GNU Coreutils Manual

对应章节 0 至 5、8、14、17、19。适用范围为 上游 9.11 文档；不等同 SP4 包版本。用途为 通用工具语义与名称核对。

[https://www.gnu.org/software/coreutils/manual/coreutils.html](https://www.gnu.org/software/coreutils/manual/coreutils.html)

## S04a GNU touch invocation

对应章节 4。适用范围为 上游稳定语义。用途为 更新时间戳、按需创建文件。

[https://www.gnu.org/s/coreutils/manual/html_node/touch-invocation.html](https://www.gnu.org/s/coreutils/manual/html_node/touch-invocation.html)

## S04b GNU cp invocation

对应章节 4。适用范围为 上游稳定语义。用途为 递归、目标目录与复制行为。

[https://www.gnu.org/s/coreutils/manual/html_node/cp-invocation.html](https://www.gnu.org/s/coreutils/manual/html_node/cp-invocation.html)

## S04c GNU chmod invocation

对应章节 8。适用范围为 上游稳定语义。用途为 权限与符号链接处理。

[https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/chmod-invocation.html)

## S05 Vim User Manual

对应章节 6。适用范围为 Vim 9.2 在线帮助；基础键位通用。用途为 模式、保存和基础操作。

[https://vimhelp.org/usr_02.txt.html](https://vimhelp.org/usr_02.txt.html)

[https://vimhelp.org/usr_toc.txt.html](https://vimhelp.org/usr_toc.txt.html)

## S06 openEuler 常用技能与账户工具手册

对应章节 7、9。适用范围为 SP4 常用技能；上游账户语义。用途为 用户、组与系统管理；已核对目标机 wheel 策略和未授权拒绝；带密码的 sudo 交互未执行。

[https://docs.openeuler.org/zh/docs/24.03_LTS_SP4/server/maintenance/common_skills/common_configurations.html](https://docs.openeuler.org/zh/docs/24.03_LTS_SP4/server/maintenance/common_skills/common_configurations.html)

[https://man7.org/linux/man-pages/man8/useradd.8.html](https://man7.org/linux/man-pages/man8/useradd.8.html)

[https://man7.org/linux/man-pages/man1/su.1.html](https://man7.org/linux/man-pages/man1/su.1.html)

## S07 DNF Command Reference

对应章节 9。适用范围为 DNF 4 系列文档；目标包版本待核对。用途为 查询、安装交易与 check-update 状态。

[https://dnf.readthedocs.io/en/latest/command_ref.html](https://dnf.readthedocs.io/en/latest/command_ref.html)

## S08 RPM 官方查询手册

对应章节 9。适用范围为 RPM 6.0 在线文档；仅参考稳定查询选项。用途为 -q、-ql、-qf；不采用未核实新选项。

[https://rpm.org/docs/6.0.x/man/rpm.8](https://rpm.org/docs/6.0.x/man/rpm.8)

## S09 systemd 官方服务与执行环境手册源码

对应章节 11、16、23、24。适用范围为 上游 main，目标版本待核对。用途为 Type、ExecStart、运行身份和限制选项。

[https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.service.xml)

[https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.exec.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemd.exec.xml)

## S10 systemctl 与 journalctl 官方手册源码

对应章节 11、23、24。适用范围为 上游 main，目标版本待核对。用途为 启用、启动、重载与日志筛选。

[https://raw.githubusercontent.com/systemd/systemd/main/man/systemctl.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/systemctl.xml)

[https://raw.githubusercontent.com/systemd/systemd/main/man/journalctl.xml](https://raw.githubusercontent.com/systemd/systemd/main/man/journalctl.xml)

## S11 openEuler 网络配置与 NetworkManager 手册

对应章节 12。适用范围为 SP4 文档与上游 NetworkManager。用途为 设备、连接与 nmcli 语义。

[https://docs.openeuler.org/en/docs/24.03_LTS_SP4/server/network/network_config/network_configuration.html](https://docs.openeuler.org/en/docs/24.03_LTS_SP4/server/network/network_config/network_configuration.html)

[https://networkmanager.dev/docs/api/latest/nmcli.html](https://networkmanager.dev/docs/api/latest/nmcli.html)

## S12 Linux man-pages 与内核凭据说明

对应章节 1、4、7、8、10、12、15。适用范围为 通用 Linux；具体实现查本机手册。用途为 身份、进程、路径、权限与文件对象。

[https://man7.org/linux/man-pages/man7/credentials.7.html](https://man7.org/linux/man-pages/man7/credentials.7.html)

[https://cdn.kernel.org/doc/html/latest/security/credentials.html](https://cdn.kernel.org/doc/html/latest/security/credentials.html)

## S13 curl 官方命令文档

对应章节 12、20。适用范围为 上游文档；仅使用成熟选项。用途为 HTTP、失败状态与超时。

[https://curl.se/docs/manpage.html](https://curl.se/docs/manpage.html)

## S14 OpenSSH 官方手册

对应章节 13。适用范围为 OpenBSD 当前手册；目标机已确认 OpenSSH 9.6p1，登录、传输和限定目标的转发已验证。用途为 主机验证、密钥、scp 与端口转发。

[https://man.openbsd.org/ssh](https://man.openbsd.org/ssh)

[https://man.openbsd.org/scp](https://man.openbsd.org/scp)

[https://man.openbsd.org/ssh-keygen](https://man.openbsd.org/ssh-keygen)

## S15 GNU tar Manual

对应章节 14、20。适用范围为 上游 1.35 文档。用途为 创建、清单、提取和归档路径。

[https://www.gnu.org/software/tar/manual/tar.html](https://www.gnu.org/software/tar/manual/tar.html)

## S16 util-linux 工具手册

对应章节 15。适用范围为 上游；目标版本待核对。用途为 lsblk、挂载与卸载。

[https://man7.org/linux/man-pages/man8/lsblk.8.html](https://man7.org/linux/man-pages/man8/lsblk.8.html)

[https://man7.org/linux/man-pages/man8/mount.8.html](https://man7.org/linux/man-pages/man8/mount.8.html)

## S17 GNU Grep Manual

对应章节 18、附录 B。适用范围为 上游 3.12 文档。用途为 g/re/p 名称来源、固定字符串与正则。

[https://www.gnu.org/s/grep/manual/grep.html](https://www.gnu.org/s/grep/manual/grep.html)

## S18 GNU Findutils Manual

对应章节 18。适用范围为 上游；索引核验。用途为 find 名称匹配与 -exec；离线全文取回未成功。

[https://www.gnu.org/software/findutils/manual/html_mono/find.html](https://www.gnu.org/software/findutils/manual/html_mono/find.html)

## S19 Git 官方文档

对应章节 21。适用范围为 当前手册的基础子命令。用途为 本地仓库与提交。

[https://git-scm.com/docs/git-init](https://git-scm.com/docs/git-init)

[https://git-scm.com/docs/git-add](https://git-scm.com/docs/git-add)

[https://git-scm.com/docs/git-commit](https://git-scm.com/docs/git-commit)

## S20 JDK 21 工具与 HTTP API

对应章节 22、24。适用范围为 JDK 21。用途为 jar 入口、编译目标与 HttpServer API。

[https://docs.oracle.com/en/java/javase/21/docs/specs/man/jar.html](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jar.html)

[https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html](https://docs.oracle.com/en/java/javase/21/docs/specs/man/javac.html)

[https://docs.oracle.com/en/java/javase/21/docs/api/jdk.httpserver/com/sun/net/httpserver/HttpServer.html](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.httpserver/com/sun/net/httpserver/HttpServer.html)

## S21 Spring Boot 3.5 系统要求

对应章节 22。适用范围为 页面版本 3.5.16。用途为 Java 与 Maven 支持范围。

[https://docs.spring.io/spring-boot/3.5/system-requirements.html](https://docs.spring.io/spring-boot/3.5/system-requirements.html)

## S22 Spring Boot 首个应用教程

对应章节 22。适用范围为 页面版本 3.5.16。用途为 Maven 依赖与可执行归档插件配置。

[https://docs.spring.io/spring-boot/3.5/tutorial/first-application/index.html](https://docs.spring.io/spring-boot/3.5/tutorial/first-application/index.html)

## S23 firewalld 官方 firewall-cmd 手册

对应章节 23。适用范围为 上游；已查询目标 firewalld 配置并确认运行状态。用途为 活动 zone 查询；不推断默认开放规则。

[https://firewalld.org/documentation/man-pages/firewall-cmd.html](https://firewalld.org/documentation/man-pages/firewall-cmd.html)

## S24 SELinuxProject getenforce 手册源码

对应章节 23。适用范围为 上游；目标策略待核对。用途为 只读模式查询；不代表服务策略已通过。

[https://raw.githubusercontent.com/SELinuxProject/selinux/main/libselinux/man/man8/getenforce.8](https://raw.githubusercontent.com/SELinuxProject/selinux/main/libselinux/man/man8/getenforce.8)

## S25 Ubuntu 与 CentOS 官方项目资料

对应章节 附录 D。适用范围为 查询当日页面。用途为 跨发行版工具差异；不转抄安装命令。

[https://ubuntu.com/server/docs/how-to/software/package-management/](https://ubuntu.com/server/docs/how-to/software/package-management/)

[https://www.centos.org/centos-stream/](https://www.centos.org/centos-stream/)

## 检索限制与交叉检查

部分 GNU 页面初次直连超时，后续通过官方索引与 /s/ 路径检索。freedesktop HTML 手册取回被拒绝后改读 systemd 官方仓库手册源码。openEuler 的个别猜测路径无法取回，未把它们列成已核对正文。SP4 快速入门旧子页面含其他版本残留，本书使用新版入口并与镜像目录交叉确认，未抄写其过时版本指引。

SP4 镜像目录与文档已确认存在；2026-09-24 已完成目标虚拟机运行测试，包含包安装、普通用户权限、脚本、Java、服务部署与回滚。重启恢复、安装器重装和密码交互未验收，具体结果见 review/RUNTIME_REPORT.md 与 review/VALIDATION.md。


## S27 openEuler 中文运维文档交叉核对

对应章节 1、9、12、13、23。核对安装前提、RPM 查询、DNF 仓库查询和 SSH 基本流程。SP4 常用技能页中仍有较早版本的示例包名，使用时只核对通用语义，不把样例包版本写成本机结果。网络连接的保存格式以目标系统实际查询为准。

[SP4 服务器快速入门](https://docs.openeuler.org/zh/docs/24.03_LTS_SP4/server/quickstart/quick_start_server.html)

[SP4 常用技能](https://docs.openeuler.org/zh/docs/24.03_LTS_SP4/server/maintenance/common_skills/common_configurations.html)

[SP4 网络配置](https://docs.openeuler.org/zh/docs/24.03_LTS_SP4/server/network/network_config/network_configuration.html)

[24.03 LTS 的 DNF 管理说明](https://docs.openeuler.org/zh/docs/24.03_LTS/docs/Administration/使用DNF管理软件包.html)

最后一项属于 24.03 LTS 文档，提供配置位置与工具概念参考，不用其中其他发行版本的源地址替换 SP4 软件源。

## S28 GNU 目标目录语义

对应章节 4、24。核对 ln 与 mv 的 -T，把软链接路径当作目标条目，避免进入它指向的目录。只使用长期支持的选项，未引入当前上游新增的交换接口。

[GNU 目标目录选项](https://www.gnu.org/software/coreutils/manual/html_node/Target-directory.html)

[GNU ln 说明](https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html)

## S29 SSH 转发失败与 HTTP 响应

对应章节 13、20、22、24。核对转发监听建立失败时的退出行为，以及 405 的 Allow 字段和 HEAD 无正文约定。

[OpenSSH 客户端配置](https://man.openbsd.org/ssh_config#ExitOnForwardFailure)

[HTTP 语义 RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html)


## S30 Maven 工具链选择与独立镜像配置

对应章节 22。JAVA_HOME 与 PATH 的选择依据 Apache Maven 官方安装说明；镜像匹配与设置文件依据官方镜像指南。阿里云页面只用于说明本次测试所采用镜像的提供者与地址，不作为 Linux 命令语义来源。访问日期为 2026-09-24。

[Maven 安装与 JDK 前提](https://maven.apache.org/install.html)

[Maven 镜像设置](https://maven.apache.org/guides/mini/guide-mirror-settings.html)

[阿里云 Maven 镜像说明](https://developer.aliyun.com/mirror/maven)

## S31 SSH 服务端转发策略

对应章节 13、24。核对 AllowTcpForwarding、Match 与 PermitOpen 的语义。上游默认值不能代替发行版配置；本次 SP4 实机有效值为禁用转发，限定测试用户后才完成隧道验收。

[OpenSSH sshd_config](https://man.openbsd.org/sshd_config#AllowTcpForwarding)
