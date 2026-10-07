package dev.journey;
import java.util.Map;
import org.springframework.http.*;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.*;
@RestControllerAdvice
public class Errors {
 @ExceptionHandler(IllegalStateException.class)
 ResponseEntity<?> provider(IllegalStateException ex){return ResponseEntity.status(502).body(Map.of("error",ex.getMessage()));}
 @ExceptionHandler(MethodArgumentNotValidException.class)
 ResponseEntity<?> invalid(){return ResponseEntity.badRequest().body(Map.of("error","text must contain 1 to 12000 characters"));}
}
