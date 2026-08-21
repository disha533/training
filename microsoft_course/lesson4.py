import asyncio
from typing import Annotated

from agent_framework import Agent, tool
from setup import create_gemini_client

client = create_gemini_client()


# Knowledge base
TRAVEL_KNOWLEDGE_BASE = {
    "Barcelona": (
        "Barcelona is Spain's cosmopolitan capital of Catalonia. "
        "Best visited Jan-March "
        "Known for Gaudi architecture, beaches, and food. "
        "Average daily cost: $100-200."
    ),
    "Tokyo": (
        "Tokyo is Japan's capital, mixing modern and traditional culture. "
        "Best visited April-May. "
        "Known for Shibuya, temples, sushi, and technology. "
        "Average daily cost: $200-250."
    ),
    "Paris": (
        "Paris is France's capital and a global center for art and culture. "
        "Best visited September-October. "
        "Known for the Eiffel Tower, Louvre, and cuisine. "
        "Average daily cost: $300-$400."
    ),
    "Cape Town": (
        "Cape Town is located on South Africa's southwest coast. "
        "Best visited November-December. "
        "Known for Table Mountain, wine regions, and wildlife. "
        "Average daily cost: $500-600."
    ),
}


@tool(approval_mode="never_require")
def search_travel_knowledge(
    query: Annotated[
        str,
        "Search query about a travel destination",
    ],
) -> str:
    """Search the travel knowledge base for destination information."""

    results = []

    for destination, info in TRAVEL_KNOWLEDGE_BASE.items():

        if query.lower() in destination.lower() or any(
            word in info.lower() for word in query.lower().split()
        ):
            results.append(f"{destination}: {info}")

    if results:
        return "\n\n".join(results)

    return "No matching destinations found."


agent = Agent(
    name="TravelRAGAgent",
    client=client,
    instructions="""
    You are a travel advisor.

    Before answering questions about destinations:
    1. Always search the travel knowledge base first.
    2. Base your answer on the retrieved information.
    3. Do not invent information that is not in the knowledge base.
    4. If information is unavailable, clearly say so.
    """,
    tools=[search_travel_knowledge],
)


async def main():

    response = await agent.run(
        "I want somewhere with great architecture and food. "
        "My budget is around $175 per day. "
        "What destinations would you recommend?"
    )
    print("Agent:")
    print(response)
    response = await agent.run(
        "I want somewhere in December 500 dollar budget and wildlife"
    )

    print("Agent:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
