#!/usr/bin/env python3
"""
Rate Limiter Demo for NovaSystem.

Demonstrates rate limit handling:
1. Usage tracking
2. Automatic retry with backoff
3. Batch processing
4. Quota tier awareness

Rate Limit Dimensions:
- RPM: Requests per minute
- TPM: Tokens per minute
- RPD: Requests per day

Usage:
    python rate_limiter_demo.py
    python rate_limiter_demo.py --demo batch
    python rate_limiter_demo.py --tier tier_2
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from novasystem.utils.rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    QuotaTier,
    BatchProcessor,
    create_limiter,
    TIER_LIMITS
)


# Simulated API call for demo purposes
async def simulated_api_call(prompt: str, delay: float = 0.1) -> dict:
    """Simulate an API call with configurable delay."""
    await asyncio.sleep(delay)
    return {
        "prompt": prompt[:30],
        "response": f"Response to: {prompt[:20]}...",
        "tokens": len(prompt.split()) * 2
    }


# Simulated API call that sometimes rate limits
call_count = 0
async def flaky_api_call(prompt: str) -> dict:
    """Simulate an API call that rate limits occasionally."""
    global call_count
    call_count += 1

    # Simulate rate limit on every 5th call
    if call_count % 5 == 0:
        raise Exception("429 Rate limit exceeded")

    await asyncio.sleep(0.05)
    return {"response": f"Success: {prompt[:20]}"}


async def demo_basic_limiting():
    """Demo: Basic rate limiting."""
    print("\n" + "="*60)
    print("📊 Demo: Basic Rate Limiting")
    print("="*60)

    # Create limiter with conservative limits for demo
    config = RateLimitConfig(
        rpm=10,  # 10 requests per minute
        tpm=100_000,
        rpd=1000,
        max_retries=3,
        base_delay=0.5
    )
    limiter = RateLimiter(config=config)

    print(f"\n📋 Configuration:")
    print(f"   RPM: {config.rpm}")
    print(f"   TPM: {config.tpm:,}")
    print(f"   RPD: {config.rpd:,}")

    # Make some requests
    print(f"\n🚀 Making 5 requests...")

    for i in range(5):
        # Check if we can proceed
        can_go, reason = limiter.can_proceed(estimated_tokens=100)
        print(f"\n   Request {i+1}: {'✅ Allowed' if can_go else f'⏳ {reason}'}")

        # Execute with rate limiting
        result = await limiter.execute_with_retry(
            simulated_api_call,
            f"Test prompt {i+1}",
            estimated_tokens=100
        )
        print(f"   Result: {result['response']}")

    # Show stats
    print(f"\n📊 Usage Statistics:")
    stats = limiter.get_stats()
    print(f"   Current RPM: {stats['current_rpm']}/{stats['limits']['rpm']}")
    print(f"   Requests today: {stats['usage']['requests_today']}")
    print(f"   Total tokens: {stats['usage']['total_tokens']:,}")


async def demo_decorator():
    """Demo: Using the @limit decorator."""
    print("\n" + "="*60)
    print("🎨 Demo: Decorator-Based Rate Limiting")
    print("="*60)

    limiter = RateLimiter(tier=QuotaTier.TIER_1)

    # Apply decorator
    @limiter.limit
    async def my_api_call(prompt: str) -> dict:
        return await simulated_api_call(prompt)

    print(f"\n🚀 Making decorated calls...")

    for i in range(3):
        result = await my_api_call(f"Decorated call {i+1}")
        print(f"   Call {i+1}: {result['response']}")

    limiter.log_stats()


async def demo_retry():
    """Demo: Automatic retry on rate limit errors."""
    print("\n" + "="*60)
    print("🔄 Demo: Automatic Retry with Backoff")
    print("="*60)

    global call_count
    call_count = 0

    config = RateLimitConfig(
        rpm=100,
        tpm=1_000_000,
        rpd=10_000,
        max_retries=5,
        base_delay=0.2,
        max_delay=2.0
    )
    limiter = RateLimiter(config=config)

    print(f"\n📋 Retry Configuration:")
    print(f"   Max retries: {config.max_retries}")
    print(f"   Base delay: {config.base_delay}s")
    print(f"   Max delay: {config.max_delay}s")

    print(f"\n🚀 Making calls (every 5th will fail initially)...")

    for i in range(7):
        try:
            result = await limiter.execute_with_retry(
                flaky_api_call,
                f"Retry test {i+1}"
            )
            print(f"   Call {i+1}: ✅ {result['response']}")
        except Exception as e:
            print(f"   Call {i+1}: ❌ {e}")

    print(f"\n📊 Rate limit hits: {limiter.stats.rate_limit_hits}")


async def demo_batch():
    """Demo: Batch processing with rate limiting."""
    print("\n" + "="*60)
    print("📦 Demo: Batch Processing")
    print("="*60)

    limiter = RateLimiter(tier=QuotaTier.TIER_1)
    processor = BatchProcessor(
        limiter=limiter,
        max_concurrent=5,
        batch_size=10
    )

    # Create batch of items
    items = [f"Batch item {i}" for i in range(15)]

    print(f"\n📋 Batch Configuration:")
    print(f"   Items: {len(items)}")
    print(f"   Max concurrent: 5")

    def progress_callback(completed: int, total: int):
        percent = (completed / total) * 100
        print(f"   Progress: {completed}/{total} ({percent:.0f}%)")

    print(f"\n🚀 Processing batch...")

    results = await processor.process_batch(
        items=items,
        processor=simulated_api_call,
        on_progress=progress_callback
    )

    # Count successes and errors
    successes = sum(1 for r in results if r and "error" not in r)
    errors = len(results) - successes

    print(f"\n📊 Results:")
    print(f"   Successes: {successes}")
    print(f"   Errors: {errors}")


async def demo_tiers():
    """Demo: Different quota tiers."""
    print("\n" + "="*60)
    print("🎚️ Demo: Quota Tiers")
    print("="*60)

    print(f"\n📋 Available Tiers:\n")

    for tier, config in TIER_LIMITS.items():
        print(f"   {tier.value.upper()}:")
        print(f"      RPM: {config.rpm:,}")
        print(f"      TPM: {config.tpm:,}")
        print(f"      RPD: {config.rpd:,}")
        print()

    print("💡 Tier Qualifications:")
    print("   Free   : Eligible countries")
    print("   Tier 1 : Paid billing linked")
    print("   Tier 2 : >$250 spend + 30 days")
    print("   Tier 3 : >$1000 spend + 30 days")


async def demo_context_manager():
    """Demo: Using context manager."""
    print("\n" + "="*60)
    print("🔐 Demo: Context Manager")
    print("="*60)

    limiter = RateLimiter(tier=QuotaTier.TIER_1)

    print(f"\n🚀 Using async context manager...")

    for i in range(3):
        async with limiter.acquire(estimated_tokens=500):
            # Simulated work
            result = await simulated_api_call(f"Context call {i+1}")
            print(f"   Call {i+1}: {result['response']}")

    limiter.log_stats()


async def demo_wait_time():
    """Demo: Wait time calculation."""
    print("\n" + "="*60)
    print("⏰ Demo: Wait Time Calculation")
    print("="*60)

    # Very low RPM to trigger waiting
    config = RateLimitConfig(rpm=3, tpm=100_000, rpd=1000)
    limiter = RateLimiter(config=config)

    print(f"\n📋 Low RPM config: {config.rpm} requests/minute")
    print(f"\n🚀 Making rapid calls (will trigger waiting)...")

    for i in range(5):
        wait = limiter.get_wait_time()
        if wait > 0:
            print(f"\n   ⏳ Need to wait {wait:.2f}s before call {i+1}")

        await limiter.wait_if_needed()

        # Quick call
        result = await limiter.execute_with_retry(
            simulated_api_call,
            f"Wait test {i+1}",
            delay=0.01
        )
        print(f"   Call {i+1}: ✅ Complete")


async def run_all_demos():
    """Run all demos."""
    print("\n" + "="*60)
    print("🚀 NovaSystem Rate Limiter Demo")
    print("="*60)

    await demo_tiers()
    await demo_basic_limiting()
    await demo_decorator()
    await demo_context_manager()
    await demo_retry()
    await demo_batch()

    print("\n" + "="*60)
    print("✨ Demo complete!")
    print("="*60)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Rate Limiter Demo")
    parser.add_argument(
        "--demo",
        choices=["all", "basic", "decorator", "retry", "batch", "tiers", "context", "wait"],
        default="all",
        help="Which demo to run"
    )
    parser.add_argument(
        "--tier",
        choices=["free", "tier_1", "tier_2", "tier_3"],
        default="tier_1",
        help="Quota tier to use"
    )

    args = parser.parse_args()

    demo_map = {
        "all": run_all_demos,
        "basic": demo_basic_limiting,
        "decorator": demo_decorator,
        "retry": demo_retry,
        "batch": demo_batch,
        "tiers": demo_tiers,
        "context": demo_context_manager,
        "wait": demo_wait_time,
    }

    await demo_map[args.demo]()


if __name__ == "__main__":
    asyncio.run(main())
