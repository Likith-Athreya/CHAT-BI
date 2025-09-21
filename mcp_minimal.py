import asyncio
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ServerCapabilities

from llm.groq_client import get_llm
from database.sql import get_engine, get_db
from graph.bi_graph import build_graph
from state.bi_state import BIState

server = Server("bi-agent")
graph = None

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="query",
            description="Query your database with natural language",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "Your question about the data"}
                },
                "required": ["question"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    global graph
    
    if name != "query":
        return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    if graph is None:
        graph = build_graph(get_llm(), get_db(get_engine()), get_engine())
    
    question = arguments.get("question", "")
    if not question:
        return [TextContent(type="text", text="No question provided")]
    
    try:
        result = graph.invoke(BIState(user_query=question, sql=None, df=None, viz=None, error=None))
        
        response = []
        if result.get("error"):
            response.append(f"Error: {result['error']}")
        if result.get("sql"):
            response.append(f"SQL: {result['sql']}")
        if result.get("df") is not None and not result["df"].empty:
            response.append(f"Results:\n{result['df'].to_string(index=False)}")
        
        return [TextContent(type="text", text="\n\n".join(response) or "No results")]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    async with stdio_server() as (read, write):
        await server.run(
            read, 
            write, 
            InitializationOptions(
                server_name="bi-agent",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )
if __name__ == "__main__":
    asyncio.run(main())
