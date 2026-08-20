import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing")

client = genai.Client(api_key=api_key)


def get_destinations() -> list[str]:
    """Get a list of available vacation destinations."""

    return [
        "Goa",
        "Bali",
        "Maldives",
        "Paris",
    ]


def calculate_budget(days: int, daily_budget: float) -> float:
    """Calculate the total trip budget."""

    return days * daily_budget


def get_weather(city: str) -> str:
    """Get the current weather information for a city."""

    weather = {
        "Goa": "Sunny, 30°C",
        "Bali": "Sunny, 28°C",
        "Maldives": "Sunny, 29°C",
        "Paris": "Cloudy, 18°C",
    }

    return weather.get(city, f"Weather information is not available for {city}.")


get_destinations_declaration = types.FunctionDeclaration(
    name="get_destinations",
    description="Get a list of available vacation destinations.",
)
calculate_budget_declaration = types.FunctionDeclaration(
    name="calculate_budget",
    description=(
        "Calculate the total trip budget based on " "number of days and daily budget."
    ),
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "days": types.Schema(
                type="INTEGER",
                description="Number of days.",
            ),
            "daily_budget": types.Schema(
                type="NUMBER",
                description="Budget available per day.",
            ),
        },
        required=["days", "daily_budget"],
    ),
)

get_weather_declaration = types.FunctionDeclaration(
    name="get_weather",
    description="Get weather information for a city.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "city": types.Schema(
                type="STRING",
                description="Name of the city.",
            ),
        },
        required=["city"],
    ),
)
travel_tool = types.Tool(
    function_declarations=[
        get_destinations_declaration,
        calculate_budget_declaration,
        get_weather_declaration,
    ]
)

tools = [travel_tool]

user_input = input("You: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_input,
    config=types.GenerateContentConfig(tools=tools),
)

for candidate in response.candidates:

    for part in candidate.content.parts:
        if part.function_call:
            function_call = part.function_call
            print("\nGemini requested:")
            print(function_call.name)
            print("\nArguments:")
            print(function_call.args)
            if function_call.name == "get_destinations":
                result = get_destinations()
            elif function_call.name == "calculate_budget":
                result = calculate_budget(
                    days=function_call.args["days"],
                    daily_budget=function_call.args["daily_budget"],
                )
            elif function_call.name == "get_weather":
                result = get_weather(city=function_call.args["city"])
            else:
                result = "Unknown tool."
            print("\nTool result:")
            print(result)
