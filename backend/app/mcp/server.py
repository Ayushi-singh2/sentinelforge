from mcp.server import MCPServer

from app.mcp.tools import inspect_repository
from app.mcp.schemas import RepositoryRequest
from app.mcp.resources import document_resource
from app.mcp.prompts import SAFE_CODE_GENERATION_PROMPT

# Create MCP Server
server = MCPServer(
    name="SentinelForge",
    instructions="Privacy-first AI developer platform"
)


# -----------------------------
# Tool
# -----------------------------
@server.tool(
    name="inspect_repository",
    description="Inspect a source code repository."
)
def inspect_repository_tool(path: str):

    request = RepositoryRequest(path=path)

    result = inspect_repository(request)

    return result.model_dump()


# -----------------------------
# Resource
# -----------------------------
@server.resource("workspace://documents")
def documents():

    return document_resource.get_documents()


# -----------------------------
# Prompt
# -----------------------------
@server.prompt(
    name="safe_code_generation"
)
def safe_code_generation():

    return SAFE_CODE_GENERATION_PROMPT


if __name__ == "__main__":
    server.run()