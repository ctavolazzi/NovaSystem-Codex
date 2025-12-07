"""
Thinking Service for NovaSystem.

Uses Gemini's thinking capabilities for enhanced reasoning:
- Thought summaries (see the model's reasoning process)
- Thinking levels (Gemini 3: low/high)
- Thinking budgets (Gemini 2.5: token-based control)
- Streaming with incremental thought summaries

Best for:
- Complex math problems
- Multi-step reasoning
- Code generation
- Data analysis
- Logical puzzles

Requires: pip install google-genai
"""

import os
import sys
import asyncio
from datetime import datetime
from typing import Optional, List, Union, AsyncIterator, Literal
from dataclasses import dataclass, field
from enum import Enum
import logging

# Attempt to import google-genai
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None
    types = None

logger = logging.getLogger(__name__)


def think_log(emoji: str, category: str, message: str, details: dict = None):
    """Log a thinking service event with emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [THINK/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")


class ThinkingLevel(Enum):
    """Thinking levels for Gemini 3 models."""
    LOW = "low"
    HIGH = "high"


class ThinkingModel(Enum):
    """Models with thinking support."""
    GEMINI_3_PRO = "gemini-3-pro-preview"
    GEMINI_25_PRO = "gemini-2.5-pro"
    GEMINI_25_FLASH = "gemini-2.5-flash"
    GEMINI_25_FLASH_LITE = "gemini-2.5-flash-lite"


@dataclass
class ThoughtPart:
    """A part of the thinking process."""
    text: str
    is_thought: bool  # True if this is thinking, False if final answer


@dataclass
class ThinkingResult:
    """Result from a thinking request."""
    answer: str
    thought_summary: Optional[str] = None
    thoughts_token_count: Optional[int] = None
    output_token_count: Optional[int] = None
    parts: List[ThoughtPart] = field(default_factory=list)

    @property
    def total_tokens(self) -> int:
        """Total tokens used (thoughts + output)."""
        thoughts = self.thoughts_token_count or 0
        output = self.output_token_count or 0
        return thoughts + output


class ThinkingService:
    """
    Service for using Gemini's thinking capabilities.

    Features:
    - Access to thought summaries
    - Control thinking level (Gemini 3)
    - Control thinking budget (Gemini 2.5)
    - Streaming with incremental thoughts

    Usage:
        service = ThinkingService()

        # Simple request with thinking
        result = await service.think(
            "Solve: What is the sum of the first 50 prime numbers?"
        )
        print(f"Thoughts: {result.thought_summary}")
        print(f"Answer: {result.answer}")

        # Control thinking level (Gemini 3)
        result = await service.think(
            "Complex math problem...",
            thinking_level=ThinkingLevel.HIGH
        )

        # Control thinking budget (Gemini 2.5)
        result = await service.think(
            "Coding task...",
            thinking_budget=8192
        )

        # Stream with thoughts
        async for part in service.think_stream("Solve this puzzle..."):
            if part.is_thought:
                print(f"[Thinking] {part.text}")
            else:
                print(f"[Answer] {part.text}")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Union[str, ThinkingModel] = ThinkingModel.GEMINI_25_FLASH
    ):
        """
        Initialize the thinking service.

        Args:
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model to use (must support thinking)
        """
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-genai package not installed. "
                "Install with: pip install google-genai"
            )

        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=self.api_key)

        if isinstance(model, ThinkingModel):
            self.model = model.value
        else:
            self.model = model

        think_log("✅", "INIT", f"ThinkingService initialized", {
            "model": self.model
        })

    async def think(
        self,
        prompt: str,
        include_thoughts: bool = True,
        thinking_level: Optional[ThinkingLevel] = None,
        thinking_budget: Optional[int] = None,
        system_instruction: Optional[str] = None
    ) -> ThinkingResult:
        """
        Generate content with thinking enabled.

        Args:
            prompt: The prompt/question to think about
            include_thoughts: Whether to include thought summaries
            thinking_level: LOW or HIGH (Gemini 3 only)
            thinking_budget: Token budget for thinking (Gemini 2.5)
                - 0 = disable thinking
                - -1 = dynamic thinking
                - 128-32768 for Pro, 0-24576 for Flash
            system_instruction: Optional system instruction

        Returns:
            ThinkingResult with answer and thought summary
        """
        think_log("🧠", "THINK", f"Processing prompt", {
            "prompt_preview": prompt[:60],
            "include_thoughts": include_thoughts
        })

        # Build thinking config
        thinking_config = {"include_thoughts": include_thoughts}

        if thinking_level and "gemini-3" in self.model:
            thinking_config["thinking_level"] = thinking_level.value
            think_log("⚙️", "CONFIG", f"Thinking level: {thinking_level.value}")

        if thinking_budget is not None:
            thinking_config["thinking_budget"] = thinking_budget
            if thinking_budget == 0:
                think_log("⚙️", "CONFIG", "Thinking disabled")
            elif thinking_budget == -1:
                think_log("⚙️", "CONFIG", "Dynamic thinking enabled")
            else:
                think_log("⚙️", "CONFIG", f"Thinking budget: {thinking_budget} tokens")

        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(**thinking_config)
        )

        if system_instruction:
            config.system_instruction = system_instruction

        # Generate
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
        )

        # Parse response
        thought_summary = None
        answer_parts = []
        parts = []

        for part in response.candidates[0].content.parts:
            if not part.text:
                continue

            if part.thought:
                thought_summary = (thought_summary or "") + part.text
                parts.append(ThoughtPart(text=part.text, is_thought=True))
            else:
                answer_parts.append(part.text)
                parts.append(ThoughtPart(text=part.text, is_thought=False))

        answer = "".join(answer_parts)

        # Get token counts
        thoughts_tokens = getattr(response.usage_metadata, 'thoughts_token_count', None)
        output_tokens = getattr(response.usage_metadata, 'candidates_token_count', None)

        think_log("✅", "COMPLETE", f"Thinking complete", {
            "answer_length": len(answer),
            "thought_length": len(thought_summary) if thought_summary else 0,
            "thought_tokens": thoughts_tokens
        })

        return ThinkingResult(
            answer=answer,
            thought_summary=thought_summary,
            thoughts_token_count=thoughts_tokens,
            output_token_count=output_tokens,
            parts=parts
        )

    async def think_stream(
        self,
        prompt: str,
        include_thoughts: bool = True,
        thinking_level: Optional[ThinkingLevel] = None,
        thinking_budget: Optional[int] = None
    ) -> AsyncIterator[ThoughtPart]:
        """
        Stream content generation with thinking.

        Yields incremental thought summaries and answer chunks.

        Args:
            prompt: The prompt to process
            include_thoughts: Whether to include thought summaries
            thinking_level: LOW or HIGH (Gemini 3 only)
            thinking_budget: Token budget for thinking (Gemini 2.5)

        Yields:
            ThoughtPart objects (check is_thought for type)
        """
        think_log("🧠", "STREAM", f"Starting streaming think", {
            "prompt_preview": prompt[:60]
        })

        # Build thinking config
        thinking_config = {"include_thoughts": include_thoughts}

        if thinking_level and "gemini-3" in self.model:
            thinking_config["thinking_level"] = thinking_level.value

        if thinking_budget is not None:
            thinking_config["thinking_budget"] = thinking_budget

        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(**thinking_config)
        )

        # Stream in a thread
        loop = asyncio.get_event_loop()

        def stream_sync():
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=prompt,
                config=config
            ):
                for part in chunk.candidates[0].content.parts:
                    if part.text:
                        yield ThoughtPart(
                            text=part.text,
                            is_thought=bool(part.thought)
                        )

        # Wrap sync generator in async
        for part in await loop.run_in_executor(None, lambda: list(stream_sync())):
            yield part

        think_log("✅", "STREAM", "Streaming complete")

    async def solve(
        self,
        problem: str,
        problem_type: Literal["math", "logic", "code", "analysis"] = "general",
        show_work: bool = True
    ) -> ThinkingResult:
        """
        Solve a problem with appropriate thinking settings.

        Args:
            problem: The problem to solve
            problem_type: Type of problem for optimized settings
            show_work: Whether to show thought process

        Returns:
            ThinkingResult with solution
        """
        # Adjust settings based on problem type
        budgets = {
            "math": 8192,
            "logic": 4096,
            "code": 16384,
            "analysis": 8192,
            "general": None  # Dynamic
        }

        prompts = {
            "math": f"Solve this math problem step by step:\n\n{problem}",
            "logic": f"Solve this logic puzzle, showing your reasoning:\n\n{problem}",
            "code": f"Write code to solve this problem, with comments:\n\n{problem}",
            "analysis": f"Analyze this thoroughly:\n\n{problem}",
            "general": problem
        }

        think_log("🎯", "SOLVE", f"Solving {problem_type} problem")

        return await self.think(
            prompt=prompts.get(problem_type, problem),
            include_thoughts=show_work,
            thinking_budget=budgets.get(problem_type)
        )

    async def reason(
        self,
        premises: List[str],
        question: str
    ) -> ThinkingResult:
        """
        Perform logical reasoning from premises.

        Args:
            premises: List of known facts/premises
            question: Question to answer based on premises

        Returns:
            ThinkingResult with reasoning and conclusion
        """
        think_log("🔍", "REASON", f"Reasoning from {len(premises)} premises")

        prompt = "Given the following premises:\n"
        for i, p in enumerate(premises, 1):
            prompt += f"{i}. {p}\n"
        prompt += f"\nQuestion: {question}\n"
        prompt += "\nReason through this step by step and provide your conclusion."

        return await self.think(
            prompt=prompt,
            include_thoughts=True,
            thinking_budget=4096
        )

    async def debate(
        self,
        topic: str,
        position: Optional[str] = None
    ) -> ThinkingResult:
        """
        Generate a well-reasoned argument on a topic.

        Args:
            topic: The topic to debate
            position: Optional position to argue (pro/con/neutral)

        Returns:
            ThinkingResult with argument
        """
        think_log("💬", "DEBATE", f"Debating: {topic[:40]}...")

        if position:
            prompt = f"Argue {position} the following topic, using logical reasoning and evidence:\n\n{topic}"
        else:
            prompt = f"Present a balanced analysis of the following topic, considering multiple perspectives:\n\n{topic}"

        return await self.think(
            prompt=prompt,
            include_thoughts=True
        )


# Quick access functions

async def think_about(
    prompt: str,
    show_thoughts: bool = True
) -> ThinkingResult:
    """Quick function to think about something."""
    service = ThinkingService()
    return await service.think(prompt, include_thoughts=show_thoughts)


async def solve_math(problem: str) -> ThinkingResult:
    """Quick function to solve a math problem."""
    service = ThinkingService()
    return await service.solve(problem, problem_type="math")


async def solve_logic(puzzle: str) -> ThinkingResult:
    """Quick function to solve a logic puzzle."""
    service = ThinkingService()
    return await service.solve(puzzle, problem_type="logic")


async def code_solution(problem: str) -> ThinkingResult:
    """Quick function to generate code solution."""
    service = ThinkingService()
    return await service.solve(problem, problem_type="code")
