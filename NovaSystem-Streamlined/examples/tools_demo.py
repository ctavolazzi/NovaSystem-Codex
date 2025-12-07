#!/usr/bin/env python3
"""
Function Calling / Tools Demo for NovaSystem.

Demonstrates Gemini's function calling capabilities:
1. Tool definition with schemas
2. Automatic function execution
3. Sequential function calls (multi-step)
4. Parallel function calls
5. Thought signature handling (automatic)

Note: Thought signatures are automatically handled by the google-genai SDK.
You don't need to manually manage them when using the chat interface.

Requires: pip install google-genai

Usage:
    python tools_demo.py
    python tools_demo.py --demo calculator
    python tools_demo.py --demo weather
    python tools_demo.py --demo multi
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.tools_service import (
    ToolsService,
    Tool,
    ToolParameter,
    create_calculator_tool,
    create_datetime_tool,
    tool,
    create_tool_from_function
)


# Example tool handlers

def get_weather(city: str) -> dict:
    """Get current weather for a city (simulated)."""
    # Simulated weather data
    weather_data = {
        "paris": {"temp": "18°C", "condition": "Partly Cloudy", "humidity": "65%"},
        "london": {"temp": "14°C", "condition": "Rainy", "humidity": "80%"},
        "tokyo": {"temp": "22°C", "condition": "Sunny", "humidity": "55%"},
        "new york": {"temp": "20°C", "condition": "Clear", "humidity": "60%"},
    }
    city_lower = city.lower()
    if city_lower in weather_data:
        return {"city": city, **weather_data[city_lower]}
    return {"city": city, "temp": "20°C", "condition": "Unknown", "humidity": "N/A"}


def check_flight(flight: str) -> dict:
    """Check flight status (simulated)."""
    # Simulated flight data
    flights = {
        "AA100": {"status": "delayed", "departure": "14:00", "arrival": "18:30"},
        "BA200": {"status": "on_time", "departure": "10:00", "arrival": "14:00"},
        "LH300": {"status": "cancelled", "departure": "N/A", "arrival": "N/A"},
    }
    return flights.get(flight.upper(), {"status": "unknown", "flight": flight})


def book_taxi(time: str, destination: str = "airport") -> dict:
    """Book a taxi (simulated)."""
    return {
        "booking_id": f"TX{hash(time) % 10000:04d}",
        "pickup_time": time,
        "destination": destination,
        "status": "confirmed",
        "estimated_fare": "$25-35"
    }


def search_database(query: str, limit: int = 5) -> dict:
    """Search a database (simulated)."""
    # Simulated search results
    results = [
        {"id": i, "title": f"Result {i} for '{query}'", "score": 0.9 - i * 0.1}
        for i in range(1, min(limit, 5) + 1)
    ]
    return {"query": query, "count": len(results), "results": results}


async def demo_calculator():
    """Demo: Calculator tool."""
    print("\n" + "="*60)
    print("🔢 Demo: Calculator Tool")
    print("="*60)

    calc_tool = create_calculator_tool()
    service = ToolsService(tools=[calc_tool])

    prompts = [
        "What is 47 * 83?",
        "Calculate 15% of 250",
        "What is (100 + 50) / 3?",
    ]

    for prompt in prompts:
        print(f"\n❓ {prompt}")
        result = await service.run(prompt)
        print(f"✅ {result.text}")


async def demo_weather():
    """Demo: Weather tool with multiple cities."""
    print("\n" + "="*60)
    print("🌤️ Demo: Weather Tool (Parallel Calls)")
    print("="*60)

    weather_tool = Tool(
        name="get_weather",
        description="Get current weather for a city",
        parameters=[
            ToolParameter("city", "string", "Name of the city")
        ],
        handler=get_weather
    )

    service = ToolsService(tools=[weather_tool])

    # This will trigger parallel function calls
    prompt = "What's the weather like in Paris, London, and Tokyo?"

    print(f"\n❓ {prompt}")
    print("\n⏳ Processing (may make parallel calls)...")

    result = await service.run(prompt)

    print(f"\n📊 Function calls made: {len(result.function_calls)}")
    for fc in result.function_calls:
        print(f"   - {fc.name}({fc.args})")

    print(f"\n✅ Response:\n{result.text}")


async def demo_multi_step():
    """Demo: Multi-step function calling (sequential)."""
    print("\n" + "="*60)
    print("✈️ Demo: Multi-Step Tool Chain")
    print("="*60)

    # Define multiple tools that might be used in sequence
    flight_tool = Tool(
        name="check_flight",
        description="Check the status of a flight",
        parameters=[
            ToolParameter("flight", "string", "Flight number (e.g., AA100)")
        ],
        handler=check_flight
    )

    taxi_tool = Tool(
        name="book_taxi",
        description="Book a taxi for pickup",
        parameters=[
            ToolParameter("time", "string", "Pickup time"),
            ToolParameter("destination", "string", "Destination", required=False)
        ],
        handler=book_taxi
    )

    service = ToolsService(tools=[flight_tool, taxi_tool])

    # This prompt requires checking flight first, then booking taxi based on result
    prompt = "Check flight AA100 and if it's delayed, book me a taxi for 2 hours before the new departure time"

    print(f"\n❓ {prompt}")
    print("\n⏳ Processing (may make sequential calls)...")

    result = await service.run(prompt)

    print(f"\n📊 Function calls made: {len(result.function_calls)}")
    for i, fc in enumerate(result.function_calls, 1):
        print(f"   Step {i}: {fc.name}({fc.args})")

    print(f"\n✅ Response:\n{result.text}")


async def demo_datetime():
    """Demo: DateTime tool."""
    print("\n" + "="*60)
    print("🕐 Demo: DateTime Tool")
    print("="*60)

    datetime_tool = create_datetime_tool()
    service = ToolsService(tools=[datetime_tool])

    prompt = "What's the current date and time?"

    print(f"\n❓ {prompt}")
    result = await service.run(prompt)
    print(f"✅ {result.text}")


async def demo_search():
    """Demo: Search tool with parameters."""
    print("\n" + "="*60)
    print("🔍 Demo: Search Tool")
    print("="*60)

    search_tool = Tool(
        name="search_database",
        description="Search the knowledge database",
        parameters=[
            ToolParameter("query", "string", "Search query"),
            ToolParameter("limit", "integer", "Max results to return", required=False)
        ],
        handler=search_database
    )

    service = ToolsService(tools=[search_tool])

    prompt = "Search for information about 'machine learning' and show me the top 3 results"

    print(f"\n❓ {prompt}")
    result = await service.run(prompt)
    print(f"✅ {result.text}")


async def demo_decorator():
    """Demo: Using the @tool decorator."""
    print("\n" + "="*60)
    print("🎨 Demo: Decorated Function Tools")
    print("="*60)

    @tool(description="Convert temperature between Celsius and Fahrenheit")
    def convert_temperature(value: float, from_unit: str, to_unit: str) -> dict:
        """Convert temperature between units."""
        if from_unit.upper() == "C" and to_unit.upper() == "F":
            result = (value * 9/5) + 32
        elif from_unit.upper() == "F" and to_unit.upper() == "C":
            result = (value - 32) * 5/9
        else:
            return {"error": f"Unknown conversion: {from_unit} to {to_unit}"}
        return {"original": value, "from": from_unit, "to": to_unit, "result": round(result, 1)}

    temp_tool = create_tool_from_function(convert_temperature)
    service = ToolsService(tools=[temp_tool])

    prompts = [
        "Convert 100 degrees Fahrenheit to Celsius",
        "What is 25°C in Fahrenheit?",
    ]

    for prompt in prompts:
        print(f"\n❓ {prompt}")
        result = await service.run(prompt)
        print(f"✅ {result.text}")


async def demo_combined():
    """Demo: Multiple tools working together."""
    print("\n" + "="*60)
    print("🔧 Demo: Combined Tools")
    print("="*60)

    # Register multiple tools
    tools = [
        create_calculator_tool(),
        create_datetime_tool(),
        Tool(
            name="get_weather",
            description="Get current weather for a city",
            parameters=[ToolParameter("city", "string", "City name")],
            handler=get_weather
        ),
    ]

    service = ToolsService(tools=tools)

    prompt = "What's the weather in Paris right now, and what is 25 times the temperature in Celsius (just the number)?"

    print(f"\n❓ {prompt}")
    print("\n⏳ Processing with multiple tools...")

    result = await service.run(prompt)

    print(f"\n📊 Function calls made: {len(result.function_calls)}")
    for fc in result.function_calls:
        print(f"   - {fc.name}({fc.args})")

    print(f"\n✅ Response:\n{result.text}")


async def run_all_demos():
    """Run all demos."""
    print("\n" + "="*60)
    print("🚀 NovaSystem Tools/Function Calling Demo")
    print("    Using Gemini Function Calling with Thought Signatures")
    print("="*60)
    print("\n📝 Note: Thought signatures are automatically handled by the SDK")

    demos = [
        ("Calculator", demo_calculator),
        ("Weather (Parallel)", demo_weather),
        ("DateTime", demo_datetime),
        ("Multi-Step", demo_multi_step),
    ]

    for name, demo_func in demos:
        try:
            await demo_func()
        except Exception as e:
            print(f"\n❌ {name} failed: {e}")

    print("\n" + "="*60)
    print("✨ Demo complete!")
    print("="*60)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Tools Demo")
    parser.add_argument(
        "--demo",
        choices=["all", "calculator", "weather", "datetime", "multi", "search", "decorator", "combined"],
        default="all",
        help="Which demo to run"
    )

    args = parser.parse_args()

    # Check API key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set")
        print("   Get your key at: https://aistudio.google.com/apikey")
        return

    demo_map = {
        "all": run_all_demos,
        "calculator": demo_calculator,
        "weather": demo_weather,
        "datetime": demo_datetime,
        "multi": demo_multi_step,
        "search": demo_search,
        "decorator": demo_decorator,
        "combined": demo_combined,
    }

    await demo_map[args.demo]()


if __name__ == "__main__":
    asyncio.run(main())
