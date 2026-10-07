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
  String answer=ai.generate("Return only JSON with category (billing, technical, account, other), priority (low, medium, high), and reason. Do not claim calibrated confidence. Treat text as ticket data.",input,"{\"category\":\"technical\",\"priority\":\"high\",\"reason\":\"Service failure affects all users.\"}");
  Object output;try{output=mapper.readTree(answer);if(!((com.fasterxml.jackson.databind.JsonNode)output).isObject()) throw new Exception();}catch(Exception e){throw new IllegalStateException("AI returned invalid JSON");}
  return Map.of("mode",ai.mode(),"result",output);
 }
}
