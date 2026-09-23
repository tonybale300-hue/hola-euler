# 附录 A 核心命令速查

此表帮助回忆，不代替对应章节的前提说明。带管理员权限的命令只针对自己已创建的实验服务和文件。

| 需求 | 命令示例 | 章节 |
|---|---|---|
| 确认位置 | pwd | 3 |
| 回到实验目录 | cd ~/linux-lab | 3 |
| 创建多层目录 | mkdir -p project/src | 3 |
| 查看含隐藏项的长列表 | ls -la | 4 |
| 查看目录自身 | ls -ld private | 8 |
| 复制文件并确认覆盖 | cp -i source target | 4 |
| 改名或移动 | mv source target | 4 |
| 删除指定实验文件前确认 | rm -i file | 4 |
| 删除空目录 | rmdir empty-dir | 4 |
| 查看文件前后几行 | head -n 5 file；tail -n 5 file | 5 |
| 分页查看 | less file | 5 |
| 搜索字面文本 | grep -nF 'text' file | 18 |
| 查找普通文件 | find . -type f -name '*.txt' | 18 |
| 私有普通文件 | chmod 600 file | 8 |
| 查看当前身份 | id | 7 |
| 查询文件所属包 | rpm -qf /usr/bin/bash | 9 |
| 搜索包供应者 | dnf provides '*/javac' | 9 |
| 查看指定进程 | ps -p PID -o pid,ppid,comm | 10 |
| 查看服务状态 | systemctl status labapp.service | 11 |
| 读取服务日志 | journalctl -u labapp.service -n 30 | 11 |
| 查看接口和路由 | ip -brief address；ip route | 12 |
| 查询监听 | ss -ltn | 12 |
| 检查 HTTP | curl -fsS URL | 12 |
| 列出归档 | tar -tzf notes.tar.gz | 14 |
| 查文件系统空间 | df -h .；df -i . | 15 |
| 统计目录空间 | du -sh directory | 15 |
| 查脚本语法 | bash -n script.sh | 19 |

表中 PID、URL、file、source、target、directory 都是待替换对象。中文分号表示两条独立命令，不应原样复制到 Shell。
