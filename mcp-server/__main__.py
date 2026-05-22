from mcp.server.fastmcp import FastMCP

from .deepresearch import register_deepresearch


mcp = FastMCP(
    "academic-army",
    instructions=(
        "AcademicArmy MCP server. It exposes project-level tools for research, "
        "blueprint orchestration, and future AcademicArmy workflow functions."
    ),
)


register_deepresearch(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")
