#!/usr/bin/env python3
"""API Miner - Stress Test for Nova v0.2.0

Tests the full system under load:
- Traffic Control (rate limiting)
- Budget Circuit Breaker
- Usage Ledger (cost tracking)
- LLM Providers

Usage:
    python mine_apis.py                    # Use default categories
    python mine_apis.py --dry-run          # Show plan without API calls
    python mine_apis.py --categories "Finance,Weather,Machine Learning"
    python mine_apis.py --provider mock    # Use mock provider (free)
"""

import argparse
import asyncio
import json
import os
import sys
import time
from typing import List, Dict, Any

# Add parent to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core import (
    get_llm,
    get_usage_ledger,
    BudgetExceededError,
    RateLimitExceeded,
)

# =============================================================================
# CONFIGURATION
# =============================================================================

DEFAULT_CATEGORIES = ["Finance", "Weather", "Machine Learning"]

# =============================================================================
# EMBEDDED SAMPLE DATA (curated from public-apis GitHub repo)
# =============================================================================

SAMPLE_CATALOG = [
    # Finance (10 APIs)
    {"API": "Alpha Vantage", "Description": "Realtime and historical stock data", "Category": "Finance", "Link": "https://www.alphavantage.co/", "Auth": "apiKey"},
    {"API": "Finnhub", "Description": "Real-Time RESTful APIs for Stocks, Currencies, and Crypto", "Category": "Finance", "Link": "https://finnhub.io/docs/api", "Auth": "apiKey"},
    {"API": "IEX Cloud", "Description": "Realtime & Historical Stock and Market Data", "Category": "Finance", "Link": "https://iexcloud.io/docs/api/", "Auth": "apiKey"},
    {"API": "Polygon", "Description": "Historical stock market data", "Category": "Finance", "Link": "https://polygon.io/", "Auth": "apiKey"},
    {"API": "Yahoo Finance", "Description": "Real time low latency stock market data", "Category": "Finance", "Link": "https://www.yahoofinanceapi.com/", "Auth": "apiKey"},
    {"API": "CoinGecko", "Description": "Cryptocurrency Price, Market, and Developer/Social Data", "Category": "Finance", "Link": "http://www.coingecko.com/api", "Auth": "No"},
    {"API": "Binance", "Description": "Exchange for Trading Cryptocurrencies", "Category": "Finance", "Link": "https://github.com/binance/binance-spot-api-docs", "Auth": "apiKey"},
    {"API": "Plaid", "Description": "Connect with user's bank accounts and access transaction data", "Category": "Finance", "Link": "https://www.plaid.com/docs", "Auth": "apiKey"},
    {"API": "Open Exchange Rates", "Description": "Exchange rates and currency conversion", "Category": "Finance", "Link": "https://openexchangerates.org/", "Auth": "apiKey"},
    {"API": "Fixer", "Description": "Foreign exchange rates and currency conversion", "Category": "Finance", "Link": "https://fixer.io/", "Auth": "apiKey"},
    # Weather (8 APIs)
    {"API": "OpenWeatherMap", "Description": "Weather data including forecasts and historical data", "Category": "Weather", "Link": "https://openweathermap.org/api", "Auth": "apiKey"},
    {"API": "Weather API", "Description": "Weather data with astronomy and geolocation", "Category": "Weather", "Link": "https://www.weatherapi.com/", "Auth": "apiKey"},
    {"API": "Tomorrow.io", "Description": "Weather API Powered by Proprietary Technology", "Category": "Weather", "Link": "https://docs.tomorrow.io", "Auth": "apiKey"},
    {"API": "Visual Crossing", "Description": "Global historical and weather forecast data", "Category": "Weather", "Link": "https://www.visualcrossing.com/weather-api", "Auth": "apiKey"},
    {"API": "Weatherbit", "Description": "Weather forecasts, historical data, and alerts", "Category": "Weather", "Link": "https://www.weatherbit.io/api", "Auth": "apiKey"},
    {"API": "Open-Meteo", "Description": "Global weather forecast API for non-commercial use", "Category": "Weather", "Link": "https://open-meteo.com/", "Auth": "No"},
    {"API": "Storm Glass", "Description": "Global marine weather from multiple sources", "Category": "Weather", "Link": "https://stormglass.io/", "Auth": "apiKey"},
    {"API": "AQICN", "Description": "Air Quality Index Data for over 1000 cities", "Category": "Weather", "Link": "https://aqicn.org/api/", "Auth": "apiKey"},
    # Machine Learning (8 APIs)
    {"API": "OpenAI", "Description": "GPT models for text generation and analysis", "Category": "Machine Learning", "Link": "https://platform.openai.com/docs/api-reference", "Auth": "apiKey"},
    {"API": "Hugging Face", "Description": "ML models for NLP, vision, and more", "Category": "Machine Learning", "Link": "https://huggingface.co/docs/api-inference", "Auth": "apiKey"},
    {"API": "Clarifai", "Description": "Computer Vision and NLP APIs", "Category": "Machine Learning", "Link": "https://docs.clarifai.com/api-guide/api-overview", "Auth": "OAuth"},
    {"API": "Google Cloud Vision", "Description": "Image analysis and labeling", "Category": "Machine Learning", "Link": "https://cloud.google.com/vision/docs", "Auth": "apiKey"},
    {"API": "AWS Rekognition", "Description": "Image and video analysis", "Category": "Machine Learning", "Link": "https://aws.amazon.com/rekognition/", "Auth": "apiKey"},
    {"API": "Deepgram", "Description": "Speech-to-text and audio intelligence", "Category": "Machine Learning", "Link": "https://developers.deepgram.com/", "Auth": "apiKey"},
    {"API": "AssemblyAI", "Description": "Speech recognition and audio intelligence", "Category": "Machine Learning", "Link": "https://www.assemblyai.com/docs/", "Auth": "apiKey"},
    {"API": "Roboflow", "Description": "Computer vision model deployment", "Category": "Machine Learning", "Link": "https://docs.roboflow.com/", "Auth": "apiKey"},
    # Science & Math (5 APIs)
    {"API": "NASA", "Description": "NASA data including imagery and space data", "Category": "Science & Math", "Link": "https://api.nasa.gov", "Auth": "No"},
    {"API": "SpaceX", "Description": "Company, vehicle, launchpad and launch data", "Category": "Science & Math", "Link": "https://github.com/r-spacex/SpaceX-API", "Auth": "No"},
    {"API": "Wolfram Alpha", "Description": "Computational knowledge engine", "Category": "Science & Math", "Link": "https://products.wolframalpha.com/api/", "Auth": "apiKey"},
    {"API": "Numbers", "Description": "Facts about numbers", "Category": "Science & Math", "Link": "http://numbersapi.com", "Auth": "No"},
    {"API": "USGS Earthquake", "Description": "Earthquakes data real-time", "Category": "Science & Math", "Link": "https://earthquake.usgs.gov/fdsnws/event/1/", "Auth": "No"},
    # Development (4 APIs)
    {"API": "GitHub", "Description": "Repositories, code and user info", "Category": "Development", "Link": "https://docs.github.com/en/rest", "Auth": "OAuth"},
    {"API": "GitLab", "Description": "Automate GitLab interaction", "Category": "Development", "Link": "https://docs.gitlab.com/ee/api/", "Auth": "OAuth"},
    {"API": "npm Registry", "Description": "Node.js package information", "Category": "Development", "Link": "https://github.com/npm/registry/blob/master/docs/REGISTRY-API.md", "Auth": "No"},
    {"API": "Libraries.io", "Description": "Open source package data", "Category": "Development", "Link": "https://libraries.io/api", "Auth": "apiKey"},
]


# =============================================================================
# DATA ACCESS
# =============================================================================


def get_catalog() -> List[Dict[str, Any]]:
    """Return the embedded API catalog."""
    print(f"📦 Using embedded catalog ({len(SAMPLE_CATALOG)} APIs)")
    return SAMPLE_CATALOG.copy()


def group_by_category(entries: List[Dict]) -> Dict[str, List[Dict]]:
    """Group API entries by category."""
    categories: Dict[str, List[Dict]] = {}
    for entry in entries:
        cat = entry.get("Category", "Uncategorized")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(entry)
    return categories


# =============================================================================
# MINING LOGIC
# =============================================================================


async def mine_category(
    category: str,
    apis: List[Dict],
    provider_name: str = "mock",
    max_apis: int = 10,
) -> Dict[str, Any]:
    """Analyze a category of APIs using Nova.

    Returns:
        Dict with results and metrics.
    """
    print(f"\n⛏️  Mining Category: {category} ({len(apis)} APIs)")

    # Construct a lean prompt to save tokens
    api_subset = apis[:max_apis]
    api_list_text = "\n".join([
        f"- {a.get('API', 'Unknown')}: {a.get('Description', 'No description')}"
        for a in api_subset
    ])

    prompt = f"""Analyze these public APIs in the '{category}' category:

{api_list_text}

Task: Identify the TOP 3 most useful APIs from this list.
For each, provide:
1. API name
2. One specific real-world use case
3. Why it stands out

Be concise (2-3 sentences per API)."""

    # Get LLM provider
    llm = get_llm(provider_name)
    if not llm.is_available():
        print(f"⚠️  Provider '{provider_name}' not available. Skipping.")
        return {"category": category, "status": "skipped", "reason": "provider_unavailable"}

    start_time = time.time()
    result = {
        "category": category,
        "apis_analyzed": len(api_subset),
        "status": "pending",
    }

    try:
        # Check budget before calling
        ledger = get_usage_ledger()
        ledger.check_budget(estimated_cost=0.01)  # Rough estimate

        # Make the API call
        response = await llm.chat(
            system_prompt="You are an API analyst helping developers find useful tools.",
            user_message=prompt,
            context="api_mining",
        )

        elapsed = time.time() - start_time
        result.update({
            "status": "success",
            "response": response,
            "elapsed_seconds": round(elapsed, 2),
        })

        # Show truncated response
        display_response = response[:400] + "..." if len(response) > 400 else response
        print(f"🤖 Analysis ({elapsed:.1f}s):\n{display_response}")

    except BudgetExceededError as e:
        print(f"🛑 BUDGET LIMIT HIT: {e}")
        result.update({"status": "budget_exceeded", "error": str(e)})

    except RateLimitExceeded as e:
        print(f"⏳ RATE LIMITED: Retry after {e.retry_after:.1f}s")
        result.update({"status": "rate_limited", "retry_after": e.retry_after})

    except Exception as e:
        print(f"❌ Error: {e}")
        result.update({"status": "error", "error": str(e)})

    return result


async def run_miner(
    categories: List[str],
    provider: str = "mock",
    dry_run: bool = False,
) -> None:
    """Run the mining operation."""
    print("=" * 60)
    print("  ⛏️  NOVA API MINER - v0.2.0 STRESS TEST")
    print("=" * 60)

    # 1. Get catalog
    entries = get_catalog()

    # 2. Group by category
    all_categories = group_by_category(entries)
    print(f"\n📊 Available categories: {', '.join(sorted(all_categories.keys()))}")

    # 3. Filter to target categories
    target_cats = [c for c in categories if c in all_categories]
    missing = [c for c in categories if c not in all_categories]

    if missing:
        print(f"⚠️  Categories not found: {', '.join(missing)}")

    if not target_cats:
        print("❌ No valid target categories. Exiting.")
        print(f"   Available: {', '.join(sorted(all_categories.keys()))}")
        return

    print(f"\n🎯 Targeting: {', '.join(target_cats)}")

    # Show budget status
    ledger = get_usage_ledger()
    budget = ledger.budget_status()
    print(f"\n💰 Budget Status:")
    print(f"   Hourly: ${budget['hourly_spend']:.4f} / ${budget['hourly_budget'] or 'unlimited'}")
    print(f"   Daily:  ${budget['daily_spend']:.4f} / ${budget['daily_budget'] or 'unlimited'}")

    if dry_run:
        print("\n🔍 DRY RUN MODE - No API calls will be made")
        for cat in target_cats:
            apis = all_categories[cat]
            print(f"   Would analyze: {cat} ({len(apis)} APIs)")
        return

    # 4. Process each category
    results = []
    for cat in target_cats:
        apis = all_categories[cat]
        result = await mine_category(cat, apis, provider_name=provider)
        results.append(result)

        # Check if we should stop early
        if result["status"] == "budget_exceeded":
            print("\n🛑 STOPPING: Budget limit reached")
            break

        # Small delay between categories
        await asyncio.sleep(0.5)

    # 5. Final Report
    print("\n" + "=" * 60)
    print("  📊 MINING OPERATION REPORT")
    print("=" * 60)

    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] in ("error", "budget_exceeded", "rate_limited"))

    print(f"\n📈 Results:")
    print(f"   Categories processed: {len(results)}")
    print(f"   Successful: {successful}")
    print(f"   Failed/Limited: {failed}")

    # Financial summary
    summary = ledger.summary()
    print(f"\n💰 Financial Summary:")
    total = summary.get('total_actual') or summary.get('total_estimated') or 0
    print(f"   Total Spend: ${total:.4f}")
    print(f"   Transactions: {summary.get('total_transactions', 0)}")
    drift = summary.get('average_drift_pct')
    if drift is not None:
        print(f"   Avg Drift: {drift:.1f}%")

    # Save results to JSON
    output_file = "mining_results.json"
    with open(output_file, "w") as f:
        json.dump({
            "timestamp": time.time(),
            "categories_targeted": target_cats,
            "results": results,
            "financial_summary": summary,
        }, f, indent=2, default=str)
    print(f"\n📁 Results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Mine Public APIs catalog with Nova")
    parser.add_argument(
        "--categories", "-c",
        type=str,
        default=",".join(DEFAULT_CATEGORIES),
        help="Comma-separated list of categories to analyze",
    )
    parser.add_argument(
        "--provider", "-p",
        type=str,
        default="mock",
        choices=["mock", "openai", "claude"],
        help="LLM provider to use (default: mock for free testing)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show plan without making API calls",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List all available categories and exit",
    )

    args = parser.parse_args()

    # Handle list-categories
    if args.list_categories:
        entries = get_catalog()
        categories = group_by_category(entries)
        print(f"\n📊 Available Categories ({len(categories)}):")
        for cat in sorted(categories.keys()):
            print(f"   {cat} ({len(categories[cat])} APIs)")
        return

    # Parse categories
    categories = [c.strip() for c in args.categories.split(",")]

    # Run the miner
    asyncio.run(run_miner(
        categories=categories,
        provider=args.provider,
        dry_run=args.dry_run,
    ))


if __name__ == "__main__":
    main()
