# 示例使用说明

脚本与程序来自第 20、22、24 章，请先阅读对应前提。所有文件为 UTF-8 / LF。
backup-notes.sh 操作当前账户的 ~/linux-lab/notes 与 backups，不删除旧归档。check-health.sh 查询本机 8080 的 /health。
java-app 中的程序可用 JDK 21 编译，Spring Boot 项目固定 3.5.16，构建需要匹配的 Maven 与依赖访问。
labapp.service 依赖已创建的服务用户与部署目录，不能只复制单元而跳过第 24 章。
当前示例是批阅稿的一部分，目标系统实测状态见 review/VALIDATION.md。
