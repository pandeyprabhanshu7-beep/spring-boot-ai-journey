package dev.journey;
import java.util.Map;
import jakarta.validation.Valid;
import jakarta.validation.constraints.*;
import org.springframework.web.bind.annotation.*;
@RestController
@RequestMapping("/api")
public class Api {
 private final AiClient ai; private final com.fasterxml.jackson.databind.ObjectMapper mapper; 
 public Api(AiClient ai, com.fasterxml.jackson.databind.ObjectMapper mapper) {this.ai=ai;this.mapper=mapper;}
 public record Request(@NotBlank @Size(max=12000) String text) {}
 @PostMapping("/run")
 public Map<String,Object> run(@Valid @RequestBody Request request) {
  String input=request.text();
  String answer=ai.generate("Explain the user question clearly with a Java example. State uncertainty.",input,"A dependency is supplied to a class instead of constructed inside it. Constructor injection makes dependencies explicit.");
  Object output=answer;
  return Map.of("mode",ai.mode(),"result",output);
 }
}
