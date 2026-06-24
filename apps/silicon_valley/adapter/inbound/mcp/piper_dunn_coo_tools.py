from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PiperCOODunn")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 COO 던입니다"
