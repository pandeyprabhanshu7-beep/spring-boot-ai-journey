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
  String answer=ai.generate("Summarize the supplied text in three bullets. Include action items only if stated. Do not invent facts.",input,"- Team agreed to add integration tests.\n- Owner: Ravi.\n- Deadline: Friday.");
  Object output=answer;
  return Map.of("mode",ai.mode(),"result",output);
 }
}
