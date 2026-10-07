package example.atlas;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import org.springframework.web.bind.annotation.*;

@RestController
public class AskController {
    public record Question(@NotBlank @Size(max=2000) String question) {}
    private final RagService service;
    public AskController(RagService service) { this.service = service; }
    @PostMapping("/ask")
    public RagService.Answer ask(@Valid @RequestBody Question request) {
        return service.ask(request.question());
    }
}
