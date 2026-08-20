import asyncio
from typing import Annotated
from agent_framework import Agent, tool
from models.models import DestinationRecommendation
from models.models import TravelRecommendations
from setup import create_gemini_client

client = create_gemini_client()


@tool
def get_destination_details(
    destination: Annotated[
        str,
        "The destination to look up",
    ],
) -> DestinationRecommendation:
    """Get structured details about a vacation destination."""

    details = {
        "Barcelona": DestinationRecommendation(
            destination="Barcelona",
            available=True,
            best_season="May-June",
            highlights=[
                "Beach",
                "Architecture",
                "Food",
            ],
            estimated_budget_usd=2000,
        ),
        "Tokyo": DestinationRecommendation(
            destination="Tokyo",
            available=True,
            best_season="March-April",
            highlights=[
                "Culture",
                "Food",
                "Technology",
            ],
            estimated_budget_usd=2500,
        ),
        "Cape Town": DestinationRecommendation(
            destination="Cape Town",
            available=False,
            best_season="November-March",
            highlights=[
                "Nature",
                "Wine",
                "Adventure",
            ],
            estimated_budget_usd=1800,
        ),
    }

    return details.get(
        destination,
        DestinationRecommendation(
            destination=destination,
            available=False,
            best_season="Unknown",
            highlights=[],
            estimated_budget_usd=0,
        ),
    )


@tool
def get_destinations() -> list[str]:
    """Get the destinations currently supported by the booking system."""

    return [
        "Barcelona",
        "Tokyo",
        "Cape Town",
        "Vancouver",
        "Dubai",
    ]


@tool
def check_destination_availability(
    destination: Annotated[
        str,
        "The destination to check availability for",
    ],
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
    name="TravelConcierge",
    client=client,
    instructions="""
    You are a luxury travel concierge named Alex.

    Your responsibilities are:

    1. Understand the traveler's preferences.
    2. Consider their budget.
    3. Consider their preferred climate and activities.
    4. Check destination availability before making recommendations.
    5. Explain why a destination matches their preferences.

    Be warm, professional, and enthusiastic about travel.

    Do not recommend destinations that are unavailable.
    """,
    tools=[check_destination_availability, get_destinations],
)

structured_agent = Agent(
    name="StructuredTravelExpert",
    client=client,
    instructions=(
        "You are a travel expert. "
        "Recommend destinations based on traveler preferences. "
        "Use the get_destination_details tool."
    ),
    tools=[get_destination_details],
)


async def main():

    # response = await agent.run(
    #     "I'd love a week-long vacation somewhere with great food "
    #     "and history. My budget is around $2500."
    # )

    # print("Agent:", response)

    response = await structured_agent.run(
        "Recommend 3 destinations for a culture-loving traveler " "with a $2500 budget",
        options={"response_format": TravelRecommendations},
    )
    print("Agent:", response)


if __name__ == "__main__":
    asyncio.run(main())
