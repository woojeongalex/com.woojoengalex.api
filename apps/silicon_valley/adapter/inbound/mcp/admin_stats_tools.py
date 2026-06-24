from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AdminStats")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "어드민 통계 서버입니다"
