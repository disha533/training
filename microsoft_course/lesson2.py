import asyncio
from typing import Annotated

from agent_framework import Agent, tool

from setup import create_gemini_client

client = create_gemini_client()


@tool
def check_destination_availability(
    destination: Annotated[str, "The destination to check availability for"],
) -> str:
    """Check if a vacation destination is currently available for booking."""

    available = {
        "Barcelona": True,
        "Tokyo": True,
        "Cape Town": False,
        "Vancouver": True,
        "Dubai": False,
    }

    is_available = available.get(destination, False)

    return (
        f"{destination} is "
        f"{'available' if is_available else 'not available'} "
        "for booking."
    )


agent = Agent(
    name="TravelAvailabilityAgent",
    client=client,
    instructions=(
        "You are a travel booking agent. "
        "Help users check destination availability "
        "and make recommendations. "
        "Always check availability before recommending "
        "a destination."
    ),
    tools=[check_destination_availability],
)


async def main():
    session = agent.create_session()
    response = await agent.run(
        "My preferred vacation destination is Tokyo.",
        session=session,
    )
    print("Agent:", response)
    response = await agent.run(
        "What is my preferred vacation destination?",
        session=session,
    )
    print("Agent:", response)
    response = await agent.run(
        "Is it available?",
        session=session,
    )
    print("Agent:", response)


if __name__ == "__main__":
    asyncio.run(main())
