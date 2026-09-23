# 附录 C 常见报错速查

报错文字随工具版本与语言环境变化。下表保留常见英文片段和诊断方向，不声称它们是本次目标系统的逐字实测输出。

| 报错片段 | 含义与先检查的事项 |
|---|---|
| command not found | 名称无法解析为命令。先拼写，再 type、PATH 与包安装情况。 |
| No such file or directory | 路径组件或所需对象不存在，也可能缺解释器。先 pwd 与逐级路径检查。 |
| Not a directory | 路径中某个需要作为目录的部分实际是文件。用 ls -ld 查每层。 |
| Is a directory | 工具期望普通文件，却得到目录。先确认对象及工具是否支持目录。 |
| Permission denied | 权限或策略拒绝。检查 id、父目录 x、文件权限与安全上下文。 |
| Operation not permitted | 请求的操作受额外规则限制。核对身份、能力、挂载或文件属性。 |
| Directory not empty | 空目录删除工具发现仍有内容。列出隐藏项，再决定逐项处理。 |
| Read-only file system | 目标文件系统只读。查询挂载与系统日志，不靠 chmod 修复。 |
| No space left on device | 检查块空间与 inode，也检查配额等限制。不要先删除未知系统文件。 |
| Address already in use | 地址端口被占用。ss 查询并识别所属进程。 |
| Connection refused | 目标拒绝 TCP 连接。检查地址端口、监听及可能的拒绝规则。 |
| Connection timed out | 在期限内未连通。检查路由、防火墙、目标可达性与超时范围。 |
| Could not resolve host | 名称解析失败。getent hosts、DNS 配置与网络状态逐项检查。 |
| UnsupportedClassVersionError | Java 字节码版本不被当前 JVM 支持。比较编译目标与实际运行版本。 |

复现前先缩小到自己的实验对象。记录“当前身份、路径、完整命令、错误、期望结果”，比只保存一张裁掉上文的截图更容易让别人帮你诊断。不要在求助记录中留下私钥、密码或令牌。
