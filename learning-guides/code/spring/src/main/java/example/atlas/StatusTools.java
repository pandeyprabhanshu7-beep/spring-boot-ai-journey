package example.atlas;

import java.util.Set;
import org.springframework.stereotype.Component;
import org.springframework.ai.mcp.annotation.McpTool;
import org.springframework.ai.mcp.annotation.McpToolParam;

@Component
public class StatusTools {
    public record Status(String service, int ready, int desired, String source, boolean live) {}

    @McpTool(name="deployment_status",
        description="Return SYNTHETIC training status for payments or catalog. Never changes a deployment.",
        generateOutputSchema=true,
        annotations=@McpTool.McpAnnotations(readOnlyHint=true, destructiveHint=false))
    public Status deploymentStatus(
        @McpToolParam(description="Training service name: payments or catalog", required=true) String service) {
        if (!Set.of("payments", "catalog").contains(service))
            throw new IllegalArgumentException("Unknown training service");
        return new Status(service, 3, 3, "synthetic-training-fixture", false);
    }
}
