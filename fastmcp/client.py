import asyncio
from fastmcp import Client

client = Client("server.py")


async def main():
    async with client:
        tools = await client.list_tools()

        print("Available tools:")

        for tool in tools:
            print(tool.name)

        result = await client.call_tool(
            "calculate_discount",
            {
                "price": 2000,
                "discount_percent": 20
            }
        )

        print("Result:")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())