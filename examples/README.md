# 示例使用说明

脚本与程序来自第 20、22、24 章，请先阅读对应前提。所有文件为 UTF-8 / LF。
backup-notes.sh 操作当前账户的 ~/linux-lab/notes 与 backups，不删除旧归档。check-health.sh 查询本机 8080 的 /health。
wait-ready.sh 接受预期版本参数，例如 v1，最多尝试十次，只有本机根路径的 HTTP 状态和版本正文均匹配才成功；失败时检查日志，不自动循环重启服务。
java-app 中的程序可用 JDK 21 编译，Spring Boot 项目固定 3.5.16，构建需要匹配的 Maven 与依赖访问。
labapp.service 依赖已创建的服务用户与部署目录，不能只复制单元而跳过第 24 章。
当前示例属于 v0.2.0 修订审阅版。目标系统实测状态见 ../review/VALIDATION.md，静态审查和模拟测试记录见 ../review/COMMAND_REVIEW.md。
