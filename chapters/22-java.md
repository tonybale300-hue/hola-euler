# 第 22 章 Java 与 Linux

> 本章任务｜从源文件生成 JAR，验证接口后正常停止服务。

## 22.1 先准备完整的 JDK

### 22.1.1 确认运行与编译能力

JVM 是 Java Virtual Machine，执行 Java 字节码的虚拟机。JDK 是 Java Development Kit，包含开发工具及运行所需组件。只有 java 命令可用，不代表 javac 编译器也已经安装。

```bash
dnf search openjdk
dnf provides '*/javac'
dnf info java-21-openjdk-devel
```

本书选择 JDK 21 作为练习基线。java-21-openjdk-devel 是需在本机查询确认的候选开发包；官方 SP4 源码仓库可查到 Java 21 项目，但这不能代替当前 x86_64 启用仓库的二进制包验证。确认来源与交易后安装，再记录以下结果。

```bash
sudo dnf install java-21-openjdk-devel
java -version
javac -version
command -v java
command -v javac
command -v jar
```

javac 关联 Java compiler，jar 关联 Java archive。java 与 javac 应属于相容的工具链，不能只看其中一个版本。JAVA_HOME 若被构建工具使用，应指向 JDK 根目录，不是 bin/java 文件；不要从其他机器复制一个绝对目录就假定正确。

## 22.2 用标准 JDK 建立第一个 HTTP 服务

### 22.2.1 完整程序 LabServer.java

先建立目录，再在编辑器中保存完整源文件。

```bash
mkdir -p ~/linux-lab/java-app
cd ~/linux-lab/java-app
vim LabServer.java
```

程序只监听本机回环地址，提供 /health 与 / 两个 GET 接口，不依赖外部 Java 库。它是教学程序，不承担公网生产流量。

```java
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public class LabServer {
    public static void main(String[] args) throws Exception {
        int port = Integer.parseInt(
            System.getProperty("lab.port", "8080"));
        String version = "v1";
        HttpServer server = HttpServer.create(
            new InetSocketAddress("127.0.0.1", port), 0);
        server.createContext("/", exchange -> {
            String path = exchange.getRequestURI().getPath();
            int status = 200;
            String text;
            if (!exchange.getRequestMethod().equals("GET")) {
                status = 405;
                exchange.getResponseHeaders().set("Allow", "GET");
                text = "method not allowed\n";
            } else if (path.equals("/health")) {
                text = "ok\n";
            } else if (path.equals("/")) {
                text = "Hola Euler " + version + "\n";
            } else {
                status = 404;
                text = "not found\n";
            }
            byte[] body = text.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set(
                "Content-Type", "text/plain; charset=utf-8");
            if (exchange.getRequestMethod().equals("HEAD")) {
                exchange.sendResponseHeaders(status, -1);
                exchange.close();
            } else {
                exchange.sendResponseHeaders(status, body.length);
                try (var output = exchange.getResponseBody()) {
                    output.write(body);
                }
            }
            System.out.println(status + " " + path);
        });
        Runtime.getRuntime().addShutdownHook(
            new Thread(() -> server.stop(1)));
        server.start();
        System.out.println("Listening on 127.0.0.1:" + port);
    }
}
```

HttpServer 是 JDK 的轻量 HTTP API。InetSocketAddress 指定监听地址与端口。收到请求后，程序检查方法和路径，写回状态码与正文。200 表示这次请求成功，404 表示找不到路径，405 表示不接受该方法，并通过 Allow 说明支持 GET。即使拒绝 HEAD，也不发送响应正文。字符先编码成 UTF-8 字节，再把字节长度交给响应接口，避免把中文字符数误作字节数。关闭钩子在正常终止流程中停止服务，不能承诺在强制 KILL 下仍执行。

### 22.2.2 编译、打包、前台运行

```bash
cd ~/linux-lab/java-app
mkdir -p classes
javac --release 21 -d classes LabServer.java
jar --create --file app.jar --main-class LabServer \
  -C classes .
java -jar app.jar
```

--release 21 指定面向 Java 21，-d 指定字节码输出目录。jar --create 创建归档，--file 指定文件，--main-class 写入启动入口，-C classes . 把 classes 中的内容放进包。java -jar 按 JAR 的入口运行。此时程序占用前台终端，在第二个终端检查。

```bash
curl -fsS http://127.0.0.1:8080/health
curl -fsS http://127.0.0.1:8080/
ss -ltn
```

预期健康正文为 ok，根路径正文为 Hola Euler v1。确认 ss 显示的监听地址是 127.0.0.1。完成后回第一个终端 Ctrl+C，释放端口。若出现地址已使用，先查占用者，不要随意结束其他 Java 进程。

## 22.3 把同一目标换成 Spring Boot

### 22.3.1 固定一份独立项目

Spring Boot 可以组织 Web 应用及其依赖。本书固定 3.5.16 作为另一条练习路径，官方该版本文档要求至少 Java 17，JDK 21 在其声明的兼容范围内；Maven 至少 3.6.3。[S21] 这是刻意固定的教学版本，后续安全维护仍要重新核对版本支持情况。

先建立独立项目及其源码、资源目录，再创建 pom.xml。

```bash
mkdir -p ~/linux-lab/spring-lab/src/main/java/book/alex
mkdir -p ~/linux-lab/spring-lab/src/main/resources
cd ~/linux-lab/spring-lab
vim pom.xml
```

POM 是 Project Object Model，描述项目坐标、依赖与构建。下面完整配置也随 examples/spring-lab 提供。

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.5.16</version>
    <relativePath/>
  </parent>
  <groupId>book.alex</groupId>
  <artifactId>spring-lab</artifactId>
  <version>1.0.0</version>
  <properties>
    <java.version>21</java.version>
  </properties>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
  </dependencies>
  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
```

### 22.3.2 一个控制器与两个接口

在 src/main/java/book/alex/LabApplication.java 保存以下内容。package 声明必须与目录对应。

```java
package book.alex;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class LabApplication {
    public static void main(String[] args) {
        SpringApplication.run(LabApplication.class, args);
    }
    @GetMapping("/health")
    public String health() { return "ok\n"; }

    @GetMapping("/")
    public String home() { return "Hola Euler Spring\n"; }
}
```

在 src/main/resources/application.properties 写入以下两行，使默认监听仍然限制在本机。

```properties
server.address=127.0.0.1
server.port=8080
```

### 22.3.3 构建前核对 Maven

通过 dnf search maven 与 dnf info maven 确认包和版本，再按第 9 章安装。mvn 是 Maven 的命令名。运行 mvn -version 检查它实际使用的 Java。首次构建需要从配置的依赖仓库下载内容，失败时分别检查仓库、代理和证书，不能把它误判为 Linux 文件权限问题。

```bash
cd ~/linux-lab/spring-lab
mvn -version
mvn package
java -jar target/spring-lab-1.0.0.jar
```

先停止上一节占用 8080 的程序，再启动此应用。对 /health 与 / 重复 curl 检查。这个极小项目没有随附自动化单元测试，mvn package 成功只说明该构建过程通过，不能声称“业务测试全部通过”。部署可以使用标准 JDK 程序或这份 Spring Boot JAR，第 24 章主线采用前者减少下载依赖。

> 实机核验｜【待 openEuler 24.03 LTS SP4 实机验证】JDK 包、Maven 包、Spring Boot 依赖解析和两个应用的目标系统运行均需记录。其他平台编译通过也不能代替这一验收。

## 22.4 本章练习

- 不要往前翻｜JDK、JVM、javac、java 分别负责什么？
- 命令填空｜运行可执行 JAR 使用 java ______ app.jar。
- 看需求写命令｜编译 LabServer.java 到 classes，再打成带入口的 app.jar。
- 看命令猜结果｜程序只监听 127.0.0.1 时，另一台电脑直接访问虚拟机 IP 的 8080 会成功吗？
- 找错误｜编译器比运行环境新，出现字节码版本不兼容时，应比较什么？
- 无提示实操｜完成构建、前台运行、健康检查和正常停止，把系统、JDK 及产物摘要记录下来。

本章新命令为 java / Java 启动器、javac / Java compiler、jar / Java archive、mvn / Maven。复用 ss、curl、sha256sum，三天后从空构建目录重新生成产物。

资料依据见 S20、S21、S22、S29。答案见第 22 章答案。
