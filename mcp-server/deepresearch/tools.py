import os
import time

from openai import OpenAI


def deepresearch(prompt: str) -> dict:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.5-pro",
        reasoning={"effort": "high"},
        tools=[{"type": "web_search"}],
        tool_choice="auto",
        include=["web_search_call.action.sources"],
        background=True,
        input=prompt,
    )
    deadline = time.monotonic() + 3600

    while response.status in {"queued", "in_progress"}:
        if time.monotonic() > deadline:
            raise TimeoutError(f"OpenAI response did not complete within 3600 seconds; response_id={response.id}")
        time.sleep(1)
        response = client.responses.retrieve(response.id)

    return response.model_dump(mode="json")


def register_deepresearch(mcp) -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("DeepResearch MCP startup validation failed: OPENAI_API_KEY is not set in the environment or current .env")
    OpenAI()
    mcp.tool()(deepresearch)
