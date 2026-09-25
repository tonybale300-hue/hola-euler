<p align="center">
  <img src="assets/cover/hola-euler.png" alt="Hola Euler 封面，Alex 著" width="560" />
</p>

# Hola Euler

**openEuler Linux 从入门到实战 · Alex 著 · v1.0.0**

从建立第一个目录开始，学会查文件、读权限、写脚本，最后在 openEuler 虚拟机中部署一个可以检查、更新和回滚的 Java 服务。

全书包含 **25 章、150 道练习与答案、5 个附录、20 幅图示**。先完成短实验，再解释结果；复习时根据任务描述自己写命令。

> **源稿公开，限个人非商业学习。未经授权禁止转载、分发和商用。** 允许分享本仓库链接。GitHub 站内查看、Fork 等平台权限保留。完整规则见 [使用许可](LICENSE.md)；本项目不采用开源许可证。

## 下载与阅读

| 当前版本 | PDF | EPUB |
|---|---|---|
| **v1.0.0** | [下载 PDF](downloads/v1.0.0/Hola-Euler-v1.0.0.pdf?raw=true) | [下载 EPUB](downloads/v1.0.0/Hola-Euler-v1.0.0.epub?raw=true) |

PDF 适合固定页码阅读、批注和打印；EPUB 支持调整字号。点击下载原文件即可保存，文件摘要见 [SHA256 校验清单](downloads/SHA256SUMS)。仓库现已公开，任何人无需登录即可访问和下载。也可从 [v1.0.0 发布页](https://github.com/tonybale300-hue/hola-euler/releases/tag/v1.0.0) 获取附件。

[完整目录](TOC.md) · [开始阅读](chapters/00-preface.md) · [发布说明](RELEASE_NOTES.md) · [报告勘误](CONTRIBUTING.md)

## 学习顺序

| 阶段 | 章节 | 完成后能做什么 |
|---|---|---|
| 认识环境 | 0 至 3 | 确认系统、区分终端与 Shell、找到文件位置 |
| 管好文件 | 4 至 8 | 复制和编辑文件、理解用户与权限 |
| 观察系统 | 9 至 15 | 查询软件包、进程、服务、网络、SSH 与存储 |
| 组合命令 | 16 至 20 | 使用变量、重定向和搜索，写备份与健康检查脚本 |
| 完成部署 | 21 至 24 | 构建 Java 程序，用 systemd 管理服务并练习回滚 |

## 环境与实测范围

- openEuler 24.03 LTS SP4、x86_64、Bash，建议使用专用虚拟机。
- 日常操作使用普通用户，实验目录为 `~/linux-lab`；管理命令的用途在对应章节说明。
- Java 使用 JDK21。Spring Boot 为可选分支，综合项目使用标准 JDK 示例。
- 文件权限、脚本、Java、systemd、SSH 隧道、升级回滚已有主线实机记录。
- Spring Boot 使用独立镜像构建；全新安装、带密码 sudo 和重启恢复未完成，详见 [已知限制](KNOWN_ISSUES.md) 和 [运行报告](review/RUNTIME_REPORT.md)。

IP、用户、网卡、PID 与包版本应按自己的环境查询。示例属于教学材料，生产部署需要另行评估。

## 源稿、示例与构建

| 路径 | 内容 |
|---|---|
| [chapters](chapters/) | Markdown 正文 |
| [exercises](exercises/) · [answers](answers/) | 练习与答案 |
| [appendices](appendices/) | 命令速查、报错、发行版差异和学习路线 |
| [examples](examples/) | Shell、Java、Spring Boot 与 systemd 示例 |
| [assets](assets/) | 封面和图示 |
| [scripts](scripts/) | PDF、EPUB 构建及检查脚本 |
| [review](review/) | 实机证据、审查历史和发布检查 |

依赖与步骤见 [BUILDING.md](BUILDING.md)。PDF 使用本机 Windows 中文字体，字体文件不随仓库分发；EPUB 构建只需要 Python 标准库。

## 来源与协作

作者为 Alex。本书使用 AI 辅助整理资料、写作、核对与排版，保留 Human-AI Collaboration 声明。项目为独立教材，不代表 openEuler 或其他组织的官方出版物。

技术资料优先对照 openEuler、GNU、Bash、systemd 及相关工具的官方文档，对应来源见 [SOURCES.md](SOURCES.md)。

## 历史版本

旧版保留用于勘误追溯；首次阅读请使用 v1.0.0。历史 PDF 中的验证状态属于当时记录。

| 版本 | PDF | EPUB | 说明 |
|---|---|---|---|
| v0.2.2 | [下载 PDF](downloads/v0.2.2/Hola-Euler-v0.2.2.pdf?raw=true) | [下载 EPUB](downloads/v0.2.2/Hola-Euler-v0.2.2.epub?raw=true) | 更正遗漏的旧验证状态提示，运行证据沿用实机报告 |
| v0.2.1 | [下载 PDF](downloads/v0.2.1/Hola-Euler-v0.2.1.pdf?raw=true) | [下载 EPUB](downloads/v0.2.1/Hola-Euler-v0.2.1.epub?raw=true) | 实机修订版，补充运行证据与适用条件 |
| v0.2.0 | [下载 PDF](downloads/v0.2.0/Hola-Euler-v0.2.0.pdf?raw=true) | [下载 EPUB](downloads/v0.2.0/Hola-Euler-v0.2.0.epub?raw=true) | 修订命令前提、失败处理与部署等待，新增图示和提示框 |
| v0.1-review | [下载 PDF](downloads/v0.1-review/Hola-Euler-v0.1-review.pdf?raw=true) | [下载 EPUB](downloads/v0.1-review/Hola-Euler-v0.1-review.epub?raw=true) | 首轮批阅稿，保留供修订对照 |
