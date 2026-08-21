import asyncio

from agent_framework import Agent

from setup import create_gemini_client

from a2a.types import (
    Message,
    MessageSendParams,
    Part,
    Role,
    Task,
    TextPart,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.utils import new_agent_text_message


def search_flights(destination: str, departure_date: str) -> str:
    """Search available flights."""

    return f"""
Available flights to {destination} on {departure_date}:

1. IndiGo - ₹8,000
2. Air India - ₹9,500
3. Vistara - ₹10,000
"""


def book_flight(flight: str) -> str:
    """Book a flight."""

    return f"{flight} booked successfully."


def search_hotels(destination: str, stay_dates: str) -> str:
    """Search available hotels."""

    return f"""
Available hotels in {destination}:

1. Beach Resort - ₹5,000/night
2. City Hotel - ₹4,000/night
3. Ocean View Hotel - ₹6,000/night
"""


def book_hotel(hotel: str) -> str:
    """Book a hotel."""

    return f"{hotel} booked successfully."


airline_llm_agent = Agent(
    client=create_gemini_client(),
    name="AirlineAgent",
    description="Specialist agent for flight search and booking.",
    instructions="""
You are a flight-booking specialist.

When the user asks for a flight:

1. Use search_flights to find available flights.
2. Choose a suitable flight.
3. Use book_flight to book it.
4. Give a short confirmation.

Always use the tools.
Do not invent flight information.
""",
    tools=[
        search_flights,
        book_flight,
    ],
)


hotel_llm_agent = Agent(
    client=create_gemini_client(),
    name="HotelAgent",
    description="Specialist agent for hotel search and booking.",
    instructions="""
You are a hotel-booking specialist.

When the user asks for a hotel:

1. Use search_hotels to find available hotels.
2. Choose a suitable hotel.
3. Use book_hotel to book it.
4. Give a short confirmation.

Always use the tools.
Do not invent hotel information.
""",
    tools=[
        search_hotels,
        book_hotel,
    ],
)


class LLMAgentExecutor(AgentExecutor):
    """
    Connects an agent_framework Agent
    to the A2A protocol.
    """

    def __init__(self, llm_agent: Agent):
        self.llm_agent = llm_agent

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:

        # Get the user's message
        user_text = context.get_user_input()

        # Run the specialist agent
        result = await self.llm_agent.run(user_text)

        # Send the agent's response back through A2A
        await event_queue.enqueue_event(new_agent_text_message(result.text))

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        raise NotImplementedError("Cancel is not supported.")


airline_handler = DefaultRequestHandler(
    agent_executor=LLMAgentExecutor(airline_llm_agent),
    task_store=InMemoryTaskStore(),
)


hotel_handler = DefaultRequestHandler(
    agent_executor=LLMAgentExecutor(hotel_llm_agent),
    task_store=InMemoryTaskStore(),
)


async def call_a2a_agent(
    handler: DefaultRequestHandler,
    text: str,
) -> str:

    message = Message(
        message_id="1",
        role=Role.user,
        parts=[Part(root=TextPart(text=text))],
    )

    params = MessageSendParams(message=message)

    result = await handler.on_message_send(params)

    return extract_text(result)


def extract_text(result: Message | Task) -> str:

    if isinstance(result, Message):

        for part in result.parts:

            root = getattr(part, "root", part)

            if isinstance(root, TextPart):
                return root.text

    if isinstance(result, Task):

        if result.status.message:

            for part in result.status.message.parts:

                root = getattr(part, "root", part)

                if isinstance(root, TextPart):
                    return root.text

        if result.history:

            for part in result.history[-1].parts:

                root = getattr(part, "root", part)

                if isinstance(root, TextPart):
                    return root.text

    return str(result)


async def ask_airline_agent(query: str) -> str:
    """Send a flight request to the Airline Agent through A2A."""

    return await call_a2a_agent(
        airline_handler,
        query,
    )


async def ask_hotel_agent(query: str) -> str:
    """Send a hotel request to the Hotel Agent through A2A."""

    return await call_a2a_agent(
        hotel_handler,
        query,
    )


travel_agent = Agent(
    client=create_gemini_client(),
    name="TravelAgent",
    instructions="""
You are a Travel Agent.

You have two specialist agents:

1. AirlineAgent
   Use ask_airline_agent for flights.

2. HotelAgent
   Use ask_hotel_agent for hotels.

IMPORTANT:

- For flight requests, always use ask_airline_agent.
- For hotel requests, always use ask_hotel_agent.
- If the user asks for both, call both agents.
- Do not handle flights or hotels yourself.
- Give the user a clear final response.
""",
    tools=[
        ask_airline_agent,
        ask_hotel_agent,
    ],
)


async def main():

    user_request = """
    Please book a flight to New York on 30 August 2026.
    """

    print("USER:")
    print(user_request)

    result = await travel_agent.run(user_request)

    print("\nTRAVEL AGENT:")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
