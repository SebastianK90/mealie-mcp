import logging
import os
import traceback

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mealie import MealieFetcher
from prompts import register_prompts
from tools import register_all_tools

# Load environment variables first
load_dotenv()

# Get log level from environment variable with INFO as default
log_level_name = os.getenv("LOG_LEVEL", "INFO")
log_level = getattr(logging, log_level_name.upper(), logging.INFO)

# Configure logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("mealie-mcp")

transport = os.getenv("MCP_TRANSPORT", "stdio")
mcp = FastMCP("mealie")

MEALIE_BASE_URL = os.getenv("MEALIE_BASE_URL")
MEALIE_API_KEY = os.getenv("MEALIE_API_KEY")
if not MEALIE_BASE_URL or not MEALIE_API_KEY:
    raise ValueError(
        "MEALIE_BASE_URL and MEALIE_API_KEY must be set in environment variables."
    )

try:
    mealie = MealieFetcher(
        base_url=MEALIE_BASE_URL,
        api_key=MEALIE_API_KEY,
    )
except Exception as e:
    logger.error({"message": "Failed to initialize Mealie client", "error": str(e)})
    logger.debug({"message": "Error traceback", "traceback": traceback.format_exc()})
    raise

register_prompts(mcp)
register_all_tools(mcp, mealie)

if __name__ == "__main__":
    try:
        logger.info({"message": "Starting Mealie MCP Server", "transport": transport})
        if transport == "sse":
            import uvicorn
            from starlette.applications import Starlette
            from starlette.routing import Mount, Route
            from mcp.server.sse import SseServerTransport

            secret = os.getenv("MCP_SECRET_PATH", "")
            prefix = f"/{secret}" if secret else ""
            port = int(os.getenv("PORT", "8000"))

            sse = SseServerTransport(f"{prefix}/messages/")

            async def handle_sse(scope, receive, send):
                async with sse.connect_sse(
                    scope, receive, send
                ) as (read_stream, write_stream):
                    await mcp._mcp_server.run(
                        read_stream,
                        write_stream,
                        mcp._mcp_server.create_initialization_options(),
                    )

            app = Starlette(
                routes=[
                    Route(f"{prefix}/sse", endpoint=handle_sse),
                    Mount(f"{prefix}/messages", app=sse.handle_post_message),
                ]
            )

            logger.info({"message": f"SSE endpoint at {prefix}/sse"})
            uvicorn.run(app, host="0.0.0.0", port=port)
        else:
            mcp.run(transport="stdio")
    except Exception as e:
        logger.critical(
            {"message": "Fatal error in Mealie MCP Server", "error": str(e)}
        )
        logger.debug(
            {"message": "Error traceback", "traceback": traceback.format_exc()}
        )
        raise
