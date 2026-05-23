import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from dotenv import dotenv_values


SERVER_NAME = "academic_army_mcp_tools"


parser = argparse.ArgumentParser(description="Install the AcademicArmy MCP server into Codex.")
parser.add_argument("-e", "--env", action="append", default=[], metavar="NAME=VALUE")
args = parser.parse_args()

for item in args.env:
    if "=" not in item or item.startswith("="):
        parser.error("-e/--env must be NAME=VALUE")

repo = Path(__file__).resolve().parent

env_items = {}
for name, value in dotenv_values(repo / ".env").items():
    name = name.lstrip("\ufeff")
    if name and value is not None:
        env_items[name] = value

for item in args.env:
    name, value = item.split("=", 1)
    env_items[name] = value

env_items.setdefault("PYTHONPATH", str(repo))

codex = shutil.which("codex")
if not codex:
    raise SystemExit("Could not find the codex command line tool in PATH.")

subprocess.run([codex, "mcp", "remove", SERVER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

command = [codex, "mcp", "add"]
for name, value in env_items.items():
    command += ["--env", f"{name}={value}"]
command += [SERVER_NAME, "--", str(Path(sys.executable).resolve()), "-m", "mcp-server"]

subprocess.run(command, check=True)

print(f"Installed {SERVER_NAME} with {codex}")
print(f"Python: {Path(sys.executable).resolve()}")
print(f"PYTHONPATH: {repo}")
print(f"Environment variables registered with codex --env: {len(env_items)}")
