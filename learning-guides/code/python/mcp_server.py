"""Official MCP Python SDK v2 local stdio server; synthetic read-only data."""
from mcp.server import MCPServer

mcp = MCPServer("Atlas training tools")


@mcp.tool()
def deployment_status(service: str) -> dict:
    """Return a SYNTHETIC training status for payments or catalog. Never changes a deployment."""
    if service not in {"payments", "catalog"}:
        raise ValueError("unknown training service")
    return {"service": service, "ready": 3, "desired": 3,
            "source": "synthetic-training-fixture", "live": False}


@mcp.resource("runbook://payments/7")
def payments_runbook() -> str:
    return ("Training runbook revision 7: verify migration compatibility, "
            "then restore the previous verified image digest.")


if __name__ == "__main__":
    mcp.run()  # stdio default. Logs must not be written to protocol stdout.
