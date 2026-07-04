import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import tomlkit
from dotenv import dotenv_values


SERVER_NAME = "academic_army_mcp_tools"


parser = argparse.ArgumentParser(
    description="Install the AcademicArmy MCP server into Codex."
)
parser.add_argument("-e", "--env", action="append", default=[], metavar="NAME=VALUE")
parser.add_argument(
    "--timeout",
    type=int,
    default=3600,
    metavar="SECONDS",
    help="MCP tool timeout in seconds.",
)
args = parser.parse_args()

for item in args.env:
    if "=" not in item or item.startswith("="):
        parser.error("-e/--env must be NAME=VALUE")

if args.timeout <= 0:
    parser.error("--timeout must be greater than 0")

repo = Path(__file__).resolve().parent

env_items = {}
for name, value in dotenv_values(repo / ".env").items():
    name = name.lstrip("\ufeff")
    if name and value is not None:
        env_items[name] = value

for item in args.env:
    name, value = item.split("=", 1)
    env_items[name] = value

codex = shutil.which("codex")
if not codex:
    raise SystemExit("Could not find the codex command line tool in PATH.")

subprocess.run(
    [codex, "mcp", "remove", SERVER_NAME],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

command = [codex, "mcp", "add"]
for name, value in env_items.items():
    command += ["--env", f"{name}={value}"]
command += [SERVER_NAME, "--", str(Path(sys.executable).resolve()), "-m", SERVER_NAME]

subprocess.run(command, check=True)

doctor = subprocess.run(
    [codex, "doctor", "--json"],
    check=True,
    capture_output=True,
    text=True,
)
codex_config = Path(json.loads(doctor.stdout)["checks"]["config.load"]["details"]["config.toml"])

config = tomlkit.parse(codex_config.read_text(encoding="utf-8"))
config["mcp_servers"][SERVER_NAME]["cwd"] = str(repo)
config["mcp_servers"][SERVER_NAME]["tool_timeout_sec"] = args.timeout
codex_config.write_text(tomlkit.dumps(config), encoding="utf-8")

print(f"Installed {SERVER_NAME} with {codex}")
print(f"Python: {Path(sys.executable).resolve()}")
print(f"Working directory: {repo}")
print(f"Codex config: {codex_config}")
print(f"Environment variables registered with codex --env: {len(env_items)}")
print(f"tool_timeout_sec: {args.timeout}")
