from fastmcp import FastMCP

mcp = FastMCP("Utility Server")


@mcp.tool
def calculate_discount(price: float, discount_percent: float) -> float:
    """Calculate the final price after applying a discount."""
    discount = price * (discount_percent / 100)
    return price - discount


@mcp.tool
def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius temperature to Fahrenheit."""
    return (celsius * 9 / 5) + 32


if __name__ == "__main__":
    mcp.run()