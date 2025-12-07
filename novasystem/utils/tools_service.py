"""
Tools/Function Calling Service for NovaSystem.

Provides Gemini function calling with proper thought signature handling:
- Sequential function calls (multi-step)
- Parallel function calls
- Automatic thought signature preservation
- Tool definitions with schemas

Important: Thought signatures are automatically handled by the google-genai SDK.
This module provides a clean interface for defining and using tools.

Requires: pip install google-genai
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable, Union, Awaitable
from dataclasses import dataclass, field
from enum import Enum
import logging
import inspect

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


def tools_log(emoji: str, category: str, message: str, details: dict = None):
    """Log a tools service event with emoji prefix."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"{timestamp} | {emoji} [TOOLS/{category}] {message}")
    if details:
        for key, value in details.items():
            val_str = str(value)[:80] + "..." if len(str(value)) > 80 else str(value)
            print(f"           └─ {key}: {val_str}")


@dataclass
class ToolParameter:
    """A parameter for a tool function."""
    name: str
    type: str  # string, number, integer, boolean, array, object
    description: str
    required: bool = True
    enum: Optional[List[str]] = None  # For constrained values


@dataclass
class Tool:
    """Definition of a callable tool/function."""
    name: str
    description: str
    parameters: List[ToolParameter] = field(default_factory=list)
    handler: Optional[Callable] = None  # The actual function to call

    def to_declaration(self) -> Dict[str, Any]:
        """Convert to Gemini function declaration format."""
        properties = {}
        required = []

        for param in self.parameters:
            prop = {
                "type": param.type,
                "description": param.description
            }
            if param.enum:
                prop["enum"] = param.enum
            properties[param.name] = prop
            if param.required:
                required.append(param.name)

        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }


@dataclass
class FunctionCall:
    """A function call from the model."""
    name: str
    args: Dict[str, Any]
    thought_signature: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "args": self.args,
            "has_signature": self.thought_signature is not None
        }


@dataclass
class FunctionResponse:
    """A response to a function call."""
    name: str
    response: Any


@dataclass
class ToolsResult:
    """Result from a tools request."""
    text: Optional[str] = None
    function_calls: List[FunctionCall] = field(default_factory=list)
    completed: bool = False  # True when model returns final text (no more FCs)


class ToolsService:
    """
    Service for function calling with Gemini.

    Features:
    - Define tools with schemas
    - Automatic function execution
    - Thought signature handling (automatic)
    - Sequential and parallel function calls
    - Multi-step tool chains

    Important: The google-genai SDK automatically handles thought signatures.
    You don't need to manually manage them - just use the chat interface.

    Usage:
        # Define tools
        weather_tool = Tool(
            name="get_weather",
            description="Get current weather for a city",
            parameters=[
                ToolParameter("city", "string", "City name"),
            ],
            handler=get_weather_func
        )

        # Create service with tools
        service = ToolsService(tools=[weather_tool])

        # Run with automatic tool execution
        result = await service.run("What's the weather in Paris?")
        print(result.text)

        # Or manual tool handling
        result = await service.call("What's the weather in Paris?")
        for fc in result.function_calls:
            # Execute function and continue...
    """

    def __init__(
        self,
        tools: List[Tool] = None,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash"
    ):
        """
        Initialize the tools service.

        Args:
            tools: List of tool definitions
            api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
            model: Model to use
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
        self.model = model
        self.tools: Dict[str, Tool] = {}

        if tools:
            for tool in tools:
                self.register_tool(tool)

        tools_log("✅", "INIT", f"ToolsService initialized", {
            "model": self.model,
            "tools": len(self.tools)
        })

    def register_tool(self, tool: Tool) -> None:
        """Register a tool."""
        self.tools[tool.name] = tool
        tools_log("🔧", "REGISTER", f"Registered tool: {tool.name}")

    def register_function(
        self,
        func: Callable,
        description: Optional[str] = None
    ) -> Tool:
        """
        Register a Python function as a tool.

        Automatically extracts parameters from function signature.

        Args:
            func: The function to register
            description: Optional description (uses docstring if not provided)

        Returns:
            The created Tool
        """
        sig = inspect.signature(func)
        doc = description or func.__doc__ or f"Function {func.__name__}"

        parameters = []
        for name, param in sig.parameters.items():
            # Try to infer type from annotation
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                elif param.annotation == list:
                    param_type = "array"
                elif param.annotation == dict:
                    param_type = "object"

            parameters.append(ToolParameter(
                name=name,
                type=param_type,
                description=f"Parameter {name}",
                required=param.default == inspect.Parameter.empty
            ))

        tool = Tool(
            name=func.__name__,
            description=doc.strip(),
            parameters=parameters,
            handler=func
        )

        self.register_tool(tool)
        return tool

    def _get_tool_declarations(self) -> List[Dict]:
        """Get all tool declarations for API call."""
        return [tool.to_declaration() for tool in self.tools.values()]

    async def call(
        self,
        prompt: str,
        history: List[Dict] = None
    ) -> ToolsResult:
        """
        Make a single call that may result in function calls.

        This is the low-level method - you handle function execution.

        Args:
            prompt: User prompt
            history: Optional conversation history

        Returns:
            ToolsResult with any function calls
        """
        tools_log("📤", "CALL", f"Calling with prompt", {
            "prompt_preview": prompt[:60],
            "tools": list(self.tools.keys())
        })

        # Build contents
        contents = history or []
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        # Build tool config
        tool_config = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(**tool.to_declaration())
                for tool in self.tools.values()
            ]
        )

        # Call API
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=[tool_config]
                )
            )
        )

        # Parse response
        function_calls = []
        text_parts = []

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call:
                fc = FunctionCall(
                    name=part.function_call.name,
                    args=dict(part.function_call.args),
                    thought_signature=getattr(part, 'thought_signature', None)
                )
                function_calls.append(fc)
                tools_log("🔧", "FC", f"Function call: {fc.name}", {"args": fc.args})
            elif hasattr(part, 'text') and part.text:
                text_parts.append(part.text)

        completed = len(function_calls) == 0

        return ToolsResult(
            text="".join(text_parts) if text_parts else None,
            function_calls=function_calls,
            completed=completed
        )

    async def run(
        self,
        prompt: str,
        max_steps: int = 10
    ) -> ToolsResult:
        """
        Run a complete tool-use loop until the model returns text.

        Automatically executes registered tool handlers.

        Args:
            prompt: User prompt
            max_steps: Maximum function call steps

        Returns:
            Final ToolsResult with text response
        """
        tools_log("🚀", "RUN", f"Starting tool run", {
            "prompt_preview": prompt[:60],
            "max_steps": max_steps
        })

        # Use chat for automatic thought signature handling
        chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                tools=[types.Tool(
                    function_declarations=[
                        types.FunctionDeclaration(**tool.to_declaration())
                        for tool in self.tools.values()
                    ]
                )]
            )
        )

        # Send initial message
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: chat.send_message(prompt)
        )

        steps = 0
        all_function_calls = []

        while steps < max_steps:
            # Check for function calls
            function_calls = []
            text_parts = []

            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_calls.append(FunctionCall(
                        name=part.function_call.name,
                        args=dict(part.function_call.args),
                        thought_signature=getattr(part, 'thought_signature', None)
                    ))
                elif hasattr(part, 'text') and part.text:
                    text_parts.append(part.text)

            if not function_calls:
                # No more function calls - we're done
                tools_log("✅", "COMPLETE", f"Run completed after {steps} steps")
                return ToolsResult(
                    text="".join(text_parts) if text_parts else None,
                    function_calls=all_function_calls,
                    completed=True
                )

            all_function_calls.extend(function_calls)

            # Execute functions
            responses = []
            for fc in function_calls:
                tools_log("⚡", "EXEC", f"Executing {fc.name}", {"args": fc.args})

                tool = self.tools.get(fc.name)
                if tool and tool.handler:
                    try:
                        # Call handler
                        result = tool.handler(**fc.args)
                        if asyncio.iscoroutine(result):
                            result = await result
                        responses.append(FunctionResponse(
                            name=fc.name,
                            response=result
                        ))
                        tools_log("✅", "RESULT", f"{fc.name} returned", {
                            "result_preview": str(result)[:60]
                        })
                    except Exception as e:
                        tools_log("❌", "ERROR", f"{fc.name} failed: {e}")
                        responses.append(FunctionResponse(
                            name=fc.name,
                            response={"error": str(e)}
                        ))
                else:
                    tools_log("⚠️", "SKIP", f"No handler for {fc.name}")
                    responses.append(FunctionResponse(
                        name=fc.name,
                        response={"error": "No handler registered"}
                    ))

            # Send function responses back
            # Build response parts for the chat
            response_parts = []
            for fr in responses:
                response_parts.append(types.Part.from_function_response(
                    name=fr.name,
                    response=fr.response if isinstance(fr.response, dict) else {"result": fr.response}
                ))

            response = await loop.run_in_executor(
                None,
                lambda: chat.send_message(response_parts)
            )

            steps += 1

        tools_log("⚠️", "MAX_STEPS", f"Reached max steps ({max_steps})")
        return ToolsResult(
            text=None,
            function_calls=all_function_calls,
            completed=False
        )


# Convenience decorator for registering functions
def tool(
    name: Optional[str] = None,
    description: Optional[str] = None,
    parameters: Optional[List[ToolParameter]] = None
):
    """
    Decorator to mark a function as a tool.

    Usage:
        @tool(description="Get weather for a city")
        def get_weather(city: str) -> dict:
            return {"temp": "20C", "city": city}
    """
    def decorator(func: Callable) -> Callable:
        func._tool_info = {
            "name": name or func.__name__,
            "description": description or func.__doc__ or "",
            "parameters": parameters
        }
        return func
    return decorator


def create_tool_from_function(func: Callable) -> Tool:
    """Create a Tool from a decorated or plain function."""
    info = getattr(func, '_tool_info', {})

    sig = inspect.signature(func)
    parameters = info.get('parameters') or []

    if not parameters:
        # Auto-generate from signature
        for pname, param in sig.parameters.items():
            param_type = "string"
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == int:
                    param_type = "integer"
                elif param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"

            parameters.append(ToolParameter(
                name=pname,
                type=param_type,
                description=f"Parameter {pname}",
                required=param.default == inspect.Parameter.empty
            ))

    return Tool(
        name=info.get('name', func.__name__),
        description=info.get('description', func.__doc__ or ""),
        parameters=parameters,
        handler=func
    )


# Pre-built common tools

def create_calculator_tool() -> Tool:
    """Create a basic calculator tool."""

    def calculate(expression: str) -> dict:
        """Evaluate a mathematical expression."""
        try:
            # Safe eval for basic math
            allowed = set('0123456789+-*/().% ')
            if not all(c in allowed for c in expression):
                return {"error": "Invalid characters in expression"}
            result = eval(expression)
            return {"result": result, "expression": expression}
        except Exception as e:
            return {"error": str(e)}

    return Tool(
        name="calculate",
        description="Evaluate a mathematical expression",
        parameters=[
            ToolParameter("expression", "string", "Math expression to evaluate")
        ],
        handler=calculate
    )


def create_datetime_tool() -> Tool:
    """Create a datetime tool."""

    def get_datetime(timezone: str = "UTC") -> dict:
        """Get current date and time."""
        from datetime import datetime
        import time
        return {
            "datetime": datetime.now().isoformat(),
            "timezone": timezone,
            "timestamp": time.time()
        }

    return Tool(
        name="get_datetime",
        description="Get the current date and time",
        parameters=[
            ToolParameter("timezone", "string", "Timezone name", required=False)
        ],
        handler=get_datetime
    )


# Quick access function

async def run_with_tools(
    prompt: str,
    tools: List[Tool]
) -> str:
    """Quick function to run a prompt with tools."""
    service = ToolsService(tools=tools)
    result = await service.run(prompt)
    return result.text or "No response generated"
