from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PiperSystemGilfoyle")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 시스템 길포일입니다"
