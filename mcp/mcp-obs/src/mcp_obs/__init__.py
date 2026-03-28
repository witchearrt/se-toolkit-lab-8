"""MCP Observatory Server - VictoriaLogs and VictoriaTraces tools."""

import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

# VictoriaLogs API endpoint
VICTORIALOGS_URL = "http://victorialogs:9428"
# VictoriaTraces API endpoint (Jaeger-compatible)
VICTORIATRACES_URL = "http://victoriatraces:10428"


def create_server() -> Server:
    """Create the MCP observability server."""
    server = Server("mcp-obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available observability tools."""
        return [
            Tool(
                name="logs_search",
                description="Search logs in VictoriaLogs by query and time range",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "LogsQL query (e.g., 'severity:ERROR service.name:\"Learning Management Service\"')",
                        },
                        "minutes": {
                            "type": "integer",
                            "description": "Time range in minutes (default: 60)",
                            "default": 60,
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of log entries to return (default: 10)",
                            "default": 10,
                        },
                    },
                    "required": ["query"],
                },
            ),
            Tool(
                name="logs_error_count",
                description="Count errors per service over a time window",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "minutes": {
                            "type": "integer",
                            "description": "Time window in minutes (default: 60)",
                            "default": 60,
                        },
                    },
                },
            ),
            Tool(
                name="traces_list",
                description="List recent traces for a service",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "service": {
                            "type": "string",
                            "description": "Service name (e.g., 'Learning Management Service')",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of traces to return (default: 10)",
                            "default": 10,
                        },
                    },
                    "required": ["service"],
                },
            ),
            Tool(
                name="traces_get",
                description="Get a specific trace by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "trace_id": {
                            "type": "string",
                            "description": "Trace ID to fetch",
                        },
                    },
                    "required": ["trace_id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """Call an observability tool."""
        import httpx

        async with httpx.AsyncClient(timeout=30.0) as client:
            if name == "logs_search":
                query = arguments.get("query", "")
                minutes = arguments.get("minutes", 60)
                limit = arguments.get("limit", 10)

                logsql = f"_time:{minutes}m {query}"
                url = f"{VICTORIALOGS_URL}/select/logsql/query"
                params = {"query": logsql, "limit": limit}

                response = await client.post(url, params=params)
                response.raise_for_status()

                return [{"type": "text", "text": response.text}]

            elif name == "logs_error_count":
                minutes = arguments.get("minutes", 60)

                logsql = f"_time:{minutes}m severity:ERROR | stats by(service.name) count()"
                url = f"{VICTORIALOGS_URL}/select/logsql/query"
                params = {"query": logsql}

                response = await client.post(url, params=params)
                response.raise_for_status()

                return [{"type": "text", "text": response.text}]

            elif name == "traces_list":
                service = arguments.get("service", "")
                limit = arguments.get("limit", 10)

                url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces"
                params = {"service": service, "limit": limit}

                response = await client.get(url, params=params)
                response.raise_for_status()

                data = response.json()
                # Format trace list
                traces = data.get("data", [])
                result = []
                for trace in traces:
                    trace_id = trace.get("traceID", "unknown")
                    span_count = len(trace.get("spans", []))
                    result.append(f"Trace ID: {trace_id}, Spans: {span_count}")

                return [{"type": "text", "text": "\n".join(result) if result else "No traces found"}]

            elif name == "traces_get":
                trace_id = arguments.get("trace_id", "")

                url = f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}"

                response = await client.get(url)
                response.raise_for_status()

                data = response.json()
                # Format trace details
                traces = data.get("data", [])
                if not traces:
                    return [{"type": "text", "text": f"Trace {trace_id} not found"}]

                trace = traces[0]
                spans = trace.get("spans", [])
                result = [f"Trace: {trace_id}"]
                result.append(f"Spans: {len(spans)}")
                result.append("")

                for span in spans:
                    operation = span.get("operationName", "unknown")
                    service = span.get("process", {}).get("serviceName", "unknown")
                    duration = span.get("duration", 0) / 1000  # Convert to ms
                    tags = span.get("tags", [])
                    errors = [t for t in tags if t.get("key") == "error"]

                    status = "❌ ERROR" if errors else "✓"
                    result.append(f"  {status} {operation} ({service}) - {duration:.2f}ms")

                return [{"type": "text", "text": "\n".join(result)}]

            else:
                raise ValueError(f"Unknown tool: {name}")

    return server


async def main():
    """Run the MCP observability server."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
