# 进度

v0.2.2 验证状态勘误版，运行测试日期 2026-09-24，打包日期 2026-09-25。

- 完成第 0 至 24 章主线运行检查，包括普通用户权限、编辑器、脚本、Java、Spring Boot、systemd、SSH、升级与回滚，详见 [运行报告](review/RUNTIME_REPORT.md)。
- 修正 JDK 选择、缺失手册包、回环地址显示、SSH 转发限制和 Maven 仓库访问问题；保留默认 Maven Central 的 403 失败条件。
- 83 次虚拟机执行记录中有 6 次早期失败，均有后续修正或明确条件下的成功复测；不将重复记录当作 83 个不同的成功测试。
- 按作者要求未重启。全新 ISO 安装、普通用户带密码 sudo、专用 EPUB 阅读器兼容性与作者批阅仍未完成。
- 原 SSH 配置已恢复；服务停止并禁用，实验挂载已卸载。69 个软件包、实验账户和文件保留供复核。
- 私有仓库为 [tonybale300-hue/hola-euler](https://github.com/tonybale300-hue/hola-euler)。新版 PDF、EPUB 和历史版本均位于 downloads/；作者指定封面用于首页。
