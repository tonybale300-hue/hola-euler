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
            exchange.sendResponseHeaders(status, body.length);
            try (var output = exchange.getResponseBody()) {
                output.write(body);
            }
            System.out.println(status + " " + path);
        });
        Runtime.getRuntime().addShutdownHook(
            new Thread(() -> server.stop(1)));
        server.start();
        System.out.println("Listening on 127.0.0.1:" + port);
    }
}
