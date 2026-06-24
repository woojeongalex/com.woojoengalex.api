from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PiperDashDinesh")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 대시보드 디네시입니다"
