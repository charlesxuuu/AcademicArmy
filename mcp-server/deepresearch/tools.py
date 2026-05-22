from __future__ import annotations

import os
import time
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(".env")


def deepresearch(
    request: dict[str, Any],
    wait_for_completion: bool = True,
    timeout_seconds: float = 3600.0,
    poll_interval_seconds: float = 5.0,
) -> dict[str, Any]:
    client = OpenAI()
    response = client.responses.create(**request)
    deadline = time.monotonic() + timeout_seconds

    while wait_for_completion and response.status in {"queued", "in_progress"}:
        if time.monotonic() > deadline:
            raise TimeoutError(f"OpenAI response did not complete within {timeout_seconds} seconds; response_id={response.id}")
        time.sleep(poll_interval_seconds)
        response = client.responses.retrieve(response.id)

    return response.model_dump(mode="json")


def register_deepresearch(mcp: Any) -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("DeepResearch MCP startup validation failed: OPENAI_API_KEY is not set in the environment or current .env")
    OpenAI()
    mcp.tool()(deepresearch)
