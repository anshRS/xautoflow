from mcp.server.fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun

code_mcp = FastMCP("Coding", mount_path="/code/", message_path="/messages/", stateless_http=True)

# tool for example purpose, will add functionality later
@code_mcp.tool()
async def code_search(query: str):
    search = DuckDuckGoSearchRun()
    response = await search.ainvoke(query)
    return response
