import asyncio

from agent_framework import Agent, tool

from setup import create_gemini_client

client = create_gemini_client()


@tool
def get_destinations() -> list[str]:
    """Get a list of popular vacation destinations."""

    return [
        "Goa",
        "Bali",
        "Maldives",
        "Paris",
    ]


agent = Agent(
    name="TravelAgent",
    client=client,
    instructions=(
        "You are a helpful travel agent. "
        "Help users find their perfect vacation destination. "
        "Use the get_destinations tool when appropriate."
    ),
    tools=[get_destinations],
)


async def main():

    async for chunk in agent.run(
        "I'm looking for a warm beach destination",
        stream=True,
    ):
        print(chunk, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
