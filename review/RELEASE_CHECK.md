# v1.0.0 发布检查

2026-09-25。当前文件为第一版发布准备成果；仓库可见性保持私有，正式公开由 Alex 操作。版本号不扩大测试结论。

## 文件与许可

- 封面、扉页、README 和电子书元数据统一为《Hola Euler · openEuler Linux 从入门到实战》。
- 个人学习许可写入 LICENSE.md，版权页包含使用范围及原仓库链接。允许个人学习下载，禁止未经授权转载、分发和商用。
- GitHub 站内查看、Fork 和不可排除的法定权利保留；项目不使用“开源许可”标签。
- PDF、EPUB 同源生成；全量及本版下载摘要分别位于 downloads/SHA256SUMS 和 downloads/v1.0.0/SHA256SUMS。
- 增加 RELEASE_NOTES.md、KNOWN_ISSUES.md、CONTRIBUTING.md 和勘误 Issue 模板。

## 文件质量与命令

- 140 页 PDF 已进行全页联系表检查和版权页放大检查；没有检测到越界或替换字符，803 个链接注释。
- 110 段 Bash 语法检查、9 个模拟用例、9 份示例一致性检查通过。
- 123 个代码块与 v0.2.2 的摘要相同，实机记录沿用，不重跑有状态的虚拟机实验。
- EPUB 的 ZIP、XML、清单、阅读顺序、内部链接和锚点检查通过。
- EPUB XHTML 在 Chrome 精确 390、430、1000 像素视口抽查，中文、代码、图示及表格可显示；页面无横向溢出。未完成专用阅读器全书验收。
- 当前文件及可达 Git 历史进行了私钥头和常见 GitHub 令牌格式扫描，结果见 release-check-results.json。模式扫描不等于所有敏感信息都已穷尽检查。

## 字体

本机 SimSun、SimHei、Consolas 的 OS/2 fsType 均为 8，即可编辑文档嵌入；PDF 采用子集嵌入。没有把 Windows 字体文件提交到仓库，EPUB 未打包字体。依据为 [Microsoft 文档嵌入说明](https://learn.microsoft.com/en-us/typography/fonts/font-faq#document-embedding)。这些检查针对本机系统字体及本次文件，不代表对所有第三方素材作出保证。

## 公开时的操作

1. 核对 v1.0.0 下载文件及 LICENSE.md，确认采用当前使用规则。
2. 将仓库可见性改为 Public。历史提交和标签随仓库一起可见，旧版下载归档保留原内容。
3. 在 Releases 中检查准备好的 v1.0.0 草稿及附件，然后发布 Release。
4. 用未登录的浏览器检查 README、PDF 和 EPUB 下载，再向读者分享仓库或发布页链接。

新 ISO 安装、带密码 sudo、重启恢复和独立新手试读仍未完成，具体范围见 KNOWN_ISSUES.md。重启按作者要求继续暂缓。

许可术语依据 [OSI 定义](https://opensource.org/osd)，平台权限依据 [GitHub 许可说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。
