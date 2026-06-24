from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PiperHRBighetti")


@mcp.tool("/myself")
async def introduce_myself() -> str:
    return "파이퍼 HR 비게티입니다"
