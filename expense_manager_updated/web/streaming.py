import ndjson
from fastmcp import Client
from fastmcp.exceptions import ToolError
from google.genai import types

from agent_client.client import SERVER_URL, format_tool_output
from web.deps import get_chat


def to_ndjson_line(obj: dict) -> bytes:
    """One JSON object, encoded as an NDJSON line, using the ndjson library."""
    return (ndjson.dumps([obj], default=str) + "\n").encode("utf-8")


async def stream_turn(user_input: str):
    """
    Send a message to Gemini, run any tools it needs, and yield NDJSON
    events as they happen: tool_call -> tool_result/tool_error -> ... -> done
    """
    try:
        async with Client(SERVER_URL) as mcp_client:
            active_chat = await get_chat(mcp_client)
            response = await active_chat.send_message(user_input)

            while response.function_calls:
                response_parts = []
                for call in response.function_calls:
                    args = dict(call.args or {})
                    yield to_ndjson_line(
                        {"type": "tool_call", "name": call.name, "args": args}
                    )

                    try:
                        result = await mcp_client.call_tool(call.name, args)
                        output = format_tool_output(result.data)
                        yield to_ndjson_line(
                            {"type": "tool_result", "name": call.name, "result": output}
                        )
                    except ToolError as e:
                        output = {"error": str(e)}
                        yield to_ndjson_line(
                            {"type": "tool_error", "name": call.name, "error": str(e)}
                        )

                    response_parts.append(
                        types.Part.from_function_response(
                            name=call.name, response=output
                        )
                    )

                response = await active_chat.send_message(response_parts)

            full_text = response.text or "(no text in response)"
            yield to_ndjson_line({"type": "done", "full_text": full_text})

    except Exception as e:
        yield to_ndjson_line({"type": "error", "message": str(e)})


async def run_turn(user_input: str) -> dict:

    import json

    final_result = {"type": "error", "message": "no response"}

    async for line in stream_turn(user_input):
        event = json.loads(line.decode("utf-8"))
        if event["type"] not in ("tool_call", "tool_result", "tool_error"):

            final_result = event

    return final_result
