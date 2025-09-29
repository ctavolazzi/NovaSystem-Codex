"""
NovaSystem MCP Server Implementation.

This module implements a Model Context Protocol (MCP) server for NovaSystem,
providing tools for external clients to interact with NovaSystem's
problem-solving capabilities.
"""

import asyncio
import json
import logging
import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
)

from ..core.process import NovaProcess
from ..core.memory import MemoryManager
from ..config.models import get_default_model

logger = logging.getLogger(__name__)


class NovaMCPServer:
    """MCP Server for NovaSystem problem-solving capabilities."""

    def __init__(self, name: str = "NovaSystem"):
        """Initialize the NovaSystem MCP server."""
        self.name = name
        self.server = Server(name)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.setup_handlers()

    def setup_handlers(self):
        """Set up MCP server handlers."""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available NovaSystem tools."""
            return [
                Tool(
                    name="nova_solve_problem",
                    description="Solve a complex problem using NovaSystem's multi-agent approach",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "problem": {
                                "type": "string",
                                "description": "The problem statement to solve"
                            },
                            "domains": {
                                "type": "string",
                                "description": "Comma-separated list of expert domains (e.g., 'Technology,Business,Science')",
                                "default": "General,Technology,Business"
                            },
                            "max_iterations": {
                                "type": "integer",
                                "description": "Maximum number of iterations for the solving process",
                                "minimum": 1,
                                "maximum": 15,
                                "default": 3
                            },
                            "model": {
                                "type": "string",
                                "description": "AI model to use for problem solving",
                                "enum": ["gpt-4", "gpt-3.5-turbo", "claude-3", "claude-3-haiku", "ollama:phi3", "ollama:llama2", "ollama:gpt-oss:20b"],
                                "default": get_default_model()
                            }
                        },
                        "required": ["problem"]
                    }
                ),
                Tool(
                    name="nova_get_session_status",
                    description="Get the status of a NovaSystem session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "The session ID to check"
                            }
                        },
                        "required": ["session_id"]
                    }
                ),
                Tool(
                    name="nova_list_sessions",
                    description="List all active NovaSystem sessions",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="nova_get_session_result",
                    description="Get the result of a completed NovaSystem session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "The session ID to get results for"
                            }
                        },
                        "required": ["session_id"]
                    }
                ),
                Tool(
                    name="nova_cancel_session",
                    description="Cancel a running NovaSystem session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "The session ID to cancel"
                            }
                        },
                        "required": ["session_id"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent]:
            """Handle tool calls."""
            try:
                if name == "nova_solve_problem":
                    return await self._solve_problem(arguments)
                elif name == "nova_get_session_status":
                    return await self._get_session_status(arguments)
                elif name == "nova_list_sessions":
                    return await self._list_sessions(arguments)
                elif name == "nova_get_session_result":
                    return await self._get_session_result(arguments)
                elif name == "nova_cancel_session":
                    return await self._cancel_session(arguments)
                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]
            except Exception as e:
                logger.error(f"Error in tool call {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    async def _solve_problem(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Solve a problem using NovaSystem."""
        problem = arguments.get("problem", "")
        domains = arguments.get("domains", "General,Technology,Business")
        max_iterations = arguments.get("max_iterations", 3)
        model = arguments.get("model", get_default_model())

        if not problem.strip():
            return [TextContent(
                type="text",
                text="Error: Problem statement cannot be empty"
            )]

        # Create session
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "status": "running",
            "problem": problem,
            "domains": domains,
            "max_iterations": max_iterations,
            "model": model,
            "started_at": datetime.now().isoformat(),
            "result": None,
            "error": None
        }

        try:
            # Parse domains
            domain_list = [d.strip() for d in domains.split(",") if d.strip()]

            # Create Nova Process
            memory_manager = MemoryManager()
            nova_process = NovaProcess(
                domains=domain_list,
                model=model,
                memory_manager=memory_manager
            )

            # Run the process
            result = await nova_process.solve_problem(
                problem,
                max_iterations=max_iterations,
                stream=False
            )

            # Update session
            self.sessions[session_id]["status"] = "completed"
            self.sessions[session_id]["result"] = result

            # Format the result
            formatted_result = self._format_result(result, session_id)
            return [TextContent(
                type="text",
                text=formatted_result
            )]

        except Exception as e:
            logger.error(f"Error solving problem: {str(e)}")
            self.sessions[session_id]["status"] = "error"
            self.sessions[session_id]["error"] = str(e)
            return [TextContent(
                type="text",
                text=f"Error solving problem: {str(e)}"
            )]

    async def _get_session_status(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get session status."""
        session_id = arguments.get("session_id")

        if session_id not in self.sessions:
            return [TextContent(
                type="text",
                text=f"Session {session_id} not found"
            )]

        session = self.sessions[session_id]
        status_info = {
            "session_id": session_id,
            "status": session["status"],
            "problem": session["problem"],
            "domains": session["domains"],
            "max_iterations": session["max_iterations"],
            "model": session["model"],
            "started_at": session["started_at"]
        }

        if session["error"]:
            status_info["error"] = session["error"]

        return [TextContent(
            type="text",
            text=json.dumps(status_info, indent=2)
        )]

    async def _list_sessions(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """List all sessions."""
        if not self.sessions:
            return [TextContent(
                type="text",
                text="No active sessions"
            )]

        session_list = []
        for session_id, session in self.sessions.items():
            session_list.append({
                "session_id": session_id,
                "status": session["status"],
                "problem": session["problem"][:100] + "..." if len(session["problem"]) > 100 else session["problem"],
                "started_at": session["started_at"]
            })

        return [TextContent(
            type="text",
            text=json.dumps(session_list, indent=2)
        )]

    async def _get_session_result(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get session result."""
        session_id = arguments.get("session_id")

        if session_id not in self.sessions:
            return [TextContent(
                type="text",
                text=f"Session {session_id} not found"
            )]

        session = self.sessions[session_id]

        if session["status"] == "running":
            return [TextContent(
                type="text",
                text=f"Session {session_id} is still running"
            )]
        elif session["status"] == "error":
            return [TextContent(
                type="text",
                text=f"Session {session_id} failed with error: {session['error']}"
            )]
        elif session["status"] == "completed":
            formatted_result = self._format_result(session["result"], session_id)
            return [TextContent(
                type="text",
                text=formatted_result
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Unknown session status: {session['status']}"
            )]

    async def _cancel_session(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Cancel a session."""
        session_id = arguments.get("session_id")

        if session_id not in self.sessions:
            return [TextContent(
                type="text",
                text=f"Session {session_id} not found"
            )]

        session = self.sessions[session_id]

        if session["status"] == "running":
            session["status"] = "cancelled"
            return [TextContent(
                type="text",
                text=f"Session {session_id} cancelled"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Session {session_id} cannot be cancelled (status: {session['status']})"
            )]

    def _format_result(self, result: Dict[str, Any], session_id: str) -> str:
        """Format the Nova Process result for display."""
        if not result:
            return "No result available."

        formatted = []
        formatted.append(f"## 🚀 NovaSystem Results (Session: {session_id})\n")

        # Add final synthesis
        if "final_synthesis" in result:
            formatted.append("### 📋 Final Synthesis")
            formatted.append(result["final_synthesis"])
            formatted.append("")

        # Add final validation
        if "final_validation" in result:
            formatted.append("### ✅ Final Validation")
            formatted.append(result["final_validation"])
            formatted.append("")

        # Add iteration summary
        if "total_iterations" in result:
            formatted.append(f"### 📊 Process Summary")
            formatted.append(f"- Total Iterations: {result['total_iterations']}")
            formatted.append(f"- Process Phase: {result.get('phase', 'Unknown')}")
            formatted.append("")

        return "\n".join(formatted)

    async def run_stdio(self):
        """Run the MCP server with stdio transport."""
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.name,
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    ),
                ),
            )

    async def run_sse(self, host: str = "localhost", port: int = 3000):
        """Run the MCP server with SSE transport."""
        from mcp.server.sse import SseServerTransport

        transport = SseServerTransport(f"http://{host}:{port}")
        await self.server.run_sse(transport)


async def main():
    """Main function to run the MCP server."""
    server = NovaMCPServer()
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main())


