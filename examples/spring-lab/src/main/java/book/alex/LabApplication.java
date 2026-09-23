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
