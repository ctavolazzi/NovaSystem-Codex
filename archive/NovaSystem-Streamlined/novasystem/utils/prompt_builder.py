"""
Prompt Builder for NovaSystem.

Implements Google's Gemini prompting best practices:
- Structured prompts with XML/Markdown tags
- Few-shot examples
- System instructions for agentic workflows
- Clear constraints and output formats

Reference: https://ai.google.dev/gemini-api/docs/prompting-strategies
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class Verbosity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Tone(Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    TECHNICAL = "technical"
    CONVERSATIONAL = "conversational"


@dataclass
class Example:
    """A few-shot example for prompts."""
    input: str
    output: str
    prefix: str = ""  # e.g., "Question:", "Input:", etc.
    output_prefix: str = ""  # e.g., "Answer:", "Output:", etc.

    def format(self) -> str:
        """Format the example for inclusion in a prompt."""
        parts = []
        if self.prefix:
            parts.append(f"{self.prefix} {self.input}")
        else:
            parts.append(self.input)

        if self.output_prefix:
            parts.append(f"{self.output_prefix} {self.output}")
        else:
            parts.append(self.output)

        return "\n".join(parts)


@dataclass
class PromptConfig:
    """Configuration for prompt generation."""
    role: str = "You are a helpful AI assistant."
    verbosity: Verbosity = Verbosity.MEDIUM
    tone: Tone = Tone.TECHNICAL
    constraints: List[str] = field(default_factory=list)
    output_format: Optional[str] = None
    examples: List[Example] = field(default_factory=list)
    use_xml_tags: bool = True  # Use XML-style tags vs Markdown


class PromptBuilder:
    """
    Build structured prompts following Gemini best practices.

    Usage:
        builder = PromptBuilder()
        builder.set_role("You are a senior Python developer")
        builder.add_constraint("Only use Python 3.10+ syntax")
        builder.add_example(Example(input="...", output="..."))

        system_prompt = builder.build_system_prompt()
        user_prompt = builder.build_user_prompt(task="...", context="...")
    """

    def __init__(self, config: Optional[PromptConfig] = None):
        self.config = config or PromptConfig()

    def set_role(self, role: str) -> 'PromptBuilder':
        """Set the AI's role/persona."""
        self.config.role = role
        return self

    def set_verbosity(self, verbosity: Verbosity) -> 'PromptBuilder':
        """Set response verbosity level."""
        self.config.verbosity = verbosity
        return self

    def set_tone(self, tone: Tone) -> 'PromptBuilder':
        """Set response tone."""
        self.config.tone = tone
        return self

    def add_constraint(self, constraint: str) -> 'PromptBuilder':
        """Add a behavioral constraint."""
        self.config.constraints.append(constraint)
        return self

    def set_output_format(self, format_desc: str) -> 'PromptBuilder':
        """Define expected output format."""
        self.config.output_format = format_desc
        return self

    def add_example(self, example: Example) -> 'PromptBuilder':
        """Add a few-shot example."""
        self.config.examples.append(example)
        return self

    def _wrap_xml(self, tag: str, content: str) -> str:
        """Wrap content in XML tags."""
        return f"<{tag}>\n{content}\n</{tag}>"

    def _wrap_markdown(self, heading: str, content: str) -> str:
        """Wrap content with Markdown heading."""
        return f"# {heading}\n{content}"

    def _format_section(self, name: str, content: str) -> str:
        """Format a section using configured style."""
        if self.config.use_xml_tags:
            return self._wrap_xml(name.lower().replace(" ", "_"), content)
        else:
            return self._wrap_markdown(name, content)

    def build_system_prompt(self) -> str:
        """
        Build the system instruction prompt.

        Returns a structured prompt with role, constraints, and output format.
        """
        sections = []

        # Role section
        sections.append(self._format_section("role", self.config.role))

        # Instructions section (core reasoning framework)
        instructions = """1. **Analyze**: Understand the task and identify requirements.
2. **Plan**: Create a step-by-step approach.
3. **Execute**: Carry out the plan methodically.
4. **Validate**: Review output against the user's task.
5. **Format**: Present the answer in the requested structure."""
        sections.append(self._format_section("instructions", instructions))

        # Constraints section
        if self.config.constraints:
            constraints_text = "\n".join(f"- {c}" for c in self.config.constraints)
            sections.append(self._format_section("constraints", constraints_text))

        # Verbosity and tone
        style = f"- Verbosity: {self.config.verbosity.value}\n- Tone: {self.config.tone.value}"
        sections.append(self._format_section("style", style))

        # Output format
        if self.config.output_format:
            sections.append(self._format_section("output_format", self.config.output_format))

        return "\n\n".join(sections)

    def build_user_prompt(self,
                          task: str,
                          context: Optional[str] = None,
                          final_instruction: Optional[str] = None) -> str:
        """
        Build the user prompt with context, examples, and task.

        Args:
            task: The main task/question
            context: Optional background information or documents
            final_instruction: Optional reminder instruction at the end

        Returns:
            Structured user prompt
        """
        sections = []

        # Context first (for long context handling)
        if context:
            sections.append(self._format_section("context", context))

        # Few-shot examples
        if self.config.examples:
            examples_text = "\n\n".join(ex.format() for ex in self.config.examples)
            sections.append(self._format_section("examples", examples_text))

        # Main task
        sections.append(self._format_section("task", task))

        # Final instruction (anchoring)
        if final_instruction:
            sections.append(self._format_section("final_instruction", final_instruction))

        return "\n\n".join(sections)

    def build_messages(self,
                       task: str,
                       context: Optional[str] = None,
                       final_instruction: str = "Think step-by-step before answering.") -> List[Dict[str, str]]:
        """
        Build complete message list for API call.

        Returns:
            List of messages in OpenAI format
        """
        return [
            {"role": "system", "content": self.build_system_prompt()},
            {"role": "user", "content": self.build_user_prompt(task, context, final_instruction)}
        ]


# Pre-configured builders for common use cases

def create_problem_solver_builder() -> PromptBuilder:
    """Create a builder optimized for problem-solving tasks."""
    builder = PromptBuilder()
    builder.set_role(
        "You are an expert problem solver with deep analytical skills. "
        "You break down complex problems into manageable parts and provide "
        "clear, actionable solutions."
    )
    builder.set_verbosity(Verbosity.HIGH)
    builder.set_tone(Tone.TECHNICAL)
    builder.add_constraint("Always explain your reasoning")
    builder.add_constraint("Consider multiple perspectives")
    builder.add_constraint("Identify potential risks or limitations")
    builder.set_output_format("""Structure your response as follows:
1. **Problem Analysis**: Identify key components and constraints
2. **Approach**: Explain your solution strategy
3. **Solution**: Provide the detailed solution
4. **Considerations**: Note any limitations or alternatives""")
    return builder


def create_code_assistant_builder() -> PromptBuilder:
    """Create a builder optimized for coding assistance."""
    builder = PromptBuilder()
    builder.set_role(
        "You are a senior software engineer with expertise in multiple "
        "programming languages and software architecture."
    )
    builder.set_verbosity(Verbosity.MEDIUM)
    builder.set_tone(Tone.TECHNICAL)
    builder.add_constraint("Write clean, readable, and well-documented code")
    builder.add_constraint("Follow language-specific best practices")
    builder.add_constraint("Consider edge cases and error handling")
    builder.set_output_format("Provide code with inline comments and a brief explanation.")
    return builder


def create_summarizer_builder() -> PromptBuilder:
    """Create a builder optimized for summarization tasks."""
    builder = PromptBuilder()
    builder.set_role(
        "You are an expert at distilling complex information into clear, "
        "concise summaries while preserving key insights."
    )
    builder.set_verbosity(Verbosity.LOW)
    builder.set_tone(Tone.FORMAL)
    builder.add_constraint("Be concise but complete")
    builder.add_constraint("Preserve the most important information")
    builder.add_constraint("Use bullet points for clarity")
    return builder


def create_agentic_builder() -> PromptBuilder:
    """
    Create a builder for agentic workflows.

    Implements the recommended system instruction template for agents
    that must handle complex reasoning, planning, and execution.
    """
    builder = PromptBuilder()

    # Override with the full agentic system prompt
    builder.config.role = """You are a very strong reasoner and planner. Use these critical instructions to structure your plans, thoughts, and responses.

Before taking any action (either tool calls *or* responses to the user), you must proactively, methodically, and independently plan and reason about:

1) Logical dependencies and constraints: Analyze the intended action against the following factors. Resolve conflicts in order of importance:
    1.1) Policy-based rules, mandatory prerequisites, and constraints.
    1.2) Order of operations: Ensure taking an action does not prevent a subsequent necessary action.
    1.3) Other prerequisites (information and/or actions needed).
    1.4) Explicit user constraints or preferences.

2) Risk assessment: What are the consequences of taking the action? Will the new state cause any future issues?
    2.1) For exploratory tasks, missing *optional* parameters is a LOW risk. Prefer calling the tool with available information over asking the user.

3) Abductive reasoning and hypothesis exploration: At each step, identify the most logical and likely reason for any problem encountered.
    3.1) Look beyond immediate or obvious causes.
    3.2) Hypotheses may require additional research.
    3.3) Prioritize hypotheses based on likelihood, but do not discard less likely ones prematurely.

4) Outcome evaluation and adaptability: Does the previous observation require any changes to your plan?
    4.1) If your initial hypotheses are disproven, actively generate new ones.

5) Information availability: Incorporate all applicable sources of information.

6) Precision and Grounding: Ensure your reasoning is extremely precise and relevant.
    6.1) Verify your claims by quoting the exact applicable information.

7) Completeness: Ensure that all requirements are exhaustively incorporated into your plan.

8) Persistence and patience: Do not give up unless all reasoning is exhausted.
    8.1) On transient errors, retry. On other errors, change your strategy.

9) Inhibit your response: Only take an action after all reasoning is completed."""

    builder.set_verbosity(Verbosity.MEDIUM)
    builder.set_tone(Tone.TECHNICAL)

    return builder


# Utility functions for quick prompt generation

def quick_prompt(task: str,
                 context: Optional[str] = None,
                 role: str = "helpful AI assistant",
                 examples: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
    """
    Quickly generate a structured prompt.

    Args:
        task: The main task/question
        context: Optional context
        role: AI role description
        examples: Optional list of {"input": ..., "output": ...} dicts

    Returns:
        Message list ready for API call
    """
    builder = PromptBuilder()
    builder.set_role(f"You are a {role}.")

    if examples:
        for ex in examples:
            builder.add_example(Example(
                input=ex.get("input", ""),
                output=ex.get("output", "")
            ))

    return builder.build_messages(task, context)


def format_json_output_prompt(task: str,
                               schema: Dict[str, Any],
                               context: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Create a prompt that requests JSON output matching a schema.

    Args:
        task: The main task
        schema: Expected JSON schema or example
        context: Optional context

    Returns:
        Message list ready for API call
    """
    builder = PromptBuilder()
    builder.set_role("You are a precise data extraction assistant.")
    builder.set_verbosity(Verbosity.LOW)
    builder.add_constraint("Output ONLY valid JSON, no additional text")
    builder.add_constraint("Follow the exact schema provided")
    builder.set_output_format(f"```json\n{json.dumps(schema, indent=2)}\n```")

    return builder.build_messages(task, context)
