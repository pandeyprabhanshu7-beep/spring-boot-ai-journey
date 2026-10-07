package dev.journey;
import java.net.URI;
import java.net.http.*;
import java.time.Duration;
import java.util.*;
import com.fasterxml.jackson.databind.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
@Service
public class AiClient {
 private final ObjectMapper mapper;
 private final HttpClient http = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();
 @Value("${ai.mode}") String mode;
 @Value("${ai.key}") String key;
 @Value("${ai.model}") String model;
 public AiClient(ObjectMapper mapper) {this.mapper=mapper;}
 public String generate(String instruction,String input,String demo) {
  if (mode.equals("demo")) return demo;
  if (!mode.equals("live") || key.isBlank()) throw new IllegalStateException("Set AI_MODE=live and OPENAI_API_KEY");
  try {
   String body=mapper.writeValueAsString(Map.of("model",model,"max_completion_tokens",600,"messages",List.of(Map.of("role","system","content",instruction),Map.of("role","user","content",input))));
   HttpRequest req=HttpRequest.newBuilder(URI.create("https://api.openai.com/v1/chat/completions")).timeout(Duration.ofSeconds(30)).header("Authorization","Bearer "+key).header("Content-Type","application/json").POST(HttpRequest.BodyPublishers.ofString(body)).build();
   HttpResponse<String> res=http.send(req,HttpResponse.BodyHandlers.ofString());
   if(res.statusCode()!=200) throw new IllegalStateException("AI provider failed");
   JsonNode result=mapper.readTree(res.body()).path("choices").path(0).path("message").path("content");
   if(!result.isTextual() || result.asText().isBlank()) throw new IllegalStateException("AI returned no text");
   return result.asText();
  } catch(InterruptedException e) {Thread.currentThread().interrupt();throw new IllegalStateException("AI request interrupted");}
  catch(Exception e) {throw new IllegalStateException("AI request failed");}
 }
 public String mode(){return mode;}
}
