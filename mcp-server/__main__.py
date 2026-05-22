import argparse
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from .deepresearch import register_deepresearch


mcp = FastMCP(
    "academic-army",
    instructions=(
        "AcademicArmy MCP server. It exposes project-level tools for research, "
        "blueprint orchestration, and future AcademicArmy workflow functions."
    ),
)


if __name__ == "__main__":
    load_dotenv(".env")

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", action="append", default=[], metavar="NAME=VALUE")
    args = parser.parse_args()

    for item in args.env:
        name, separator, value = item.partition("=")
        if not separator or not name:
            parser.error("-e/--env must be NAME=VALUE")
        os.environ[name] = value

    register_deepresearch(mcp)
    mcp.run(transport="stdio")
