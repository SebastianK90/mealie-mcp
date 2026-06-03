import logging as _logging
import os
import sys
import traceback

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from mealie import MealieFetcher
from prompts import register_prompts
from tools import register_all_tools

# Load environment variables first
load_dotenv()

# Get log level from environment variable with WARNING as default.
# (stdout is reserved for MCP JSON-RPC traffic; logs MUST go to stderr.)
log_level_name = os.getenv("LOG_LEVEL", "WARNING")
log_level = getattr(_logging, log_level_name.upper(), _logging.WARNING)

# Configure logging — explicit stderr handler so logs never pollute the
# MCP JSON-RPC stdout stream and trigger ValidationError in the client.
# force=True re-initialises handlers even if FastMCP's configure_logging
# already attached a default StreamHandler(sys.stdout) above.
_logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[_logging.StreamHandler(sys.stderr)],
    force=True,
)

# --- LAYER 4: monkey-patch FastMCP's configure_logging to honour LOG_LEVEL ---
# Upstream: mcp/server/fastmcp/utilities/logging.py:19-43
#   def configure_logging(level: Literal[...] = "INFO"):
#       ...
#       logging.basicConfig(level=level, format="%(message)s", handlers=handlers)
# The hardcoded default level="INFO" is what re-asserts spam after our
# basicConfig. Replacing the function with one that reads from env fixes it.
import mcp.server.fastmcp.utilities.logging as _mcp_logging
def _patched_configure_logging(level=log_level_name.upper()) -> None:
    handlers = []
    try:
        from rich.console import Console
        from rich.logging import RichHandler
        handlers.append(RichHandler(console=Console(stderr=True),
                                    rich_tracebacks=True))
    except ImportError:
        pass
    if not handlers:
        # Default StreamHandler() lands on stdout — corrupt the JSON-RPC
        # stream. Force stderr.
        handlers.append(_logging.StreamHandler(sys.stderr))
    _logging.basicConfig(
        level=getattr(_logging, level, _logging.INFO),
        format="%(message)s",
        handlers=handlers,
        force=True,
    )
_mcp_logging.configure_logging = _patched_configure_logging
_patched_configure_logging()  # apply immediately, before FastMCP() is even called

# --- LAYER 2: helper to re-assert stderr handlers after FastMCP init ---
def _force_mcp_loggers_to_stderr():
    """Replace handlers on framework loggers so all log lines land on stderr.

    FastMCP.__init__() runs configure_logging() which attaches a default
    StreamHandler() (= stdout) to the mcp.* loggers. This function re-
    attaches our explicit stderr handler and disables propagation.
    Called AFTER `mcp = FastMCP("name")` below.
    """
    stderr_handler = _logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(_logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    for _name in ("mcp", "mcp.server", "mcp.server.lowlevel",
                  "mcp.server.fastmcp", "mcp.server.stdio"):
        _lg = _logging.getLogger(_name)
        _lg.handlers = [stderr_handler]
        _lg.propagate = False
        _lg.setLevel(log_level)

# --- LAYER 3: belt-and-braces StreamHandler default ---
_orig_init = _logging.StreamHandler.__init__
def _patched_init(self, stream=None):
    if stream is None:
        stream = sys.stderr
    _orig_init(self, stream)
_logging.StreamHandler.__init__ = _patched_init

logger = _logging.getLogger("mealie-mcp")

transport = os.getenv("MCP_TRANSPORT", "stdio")
mcp = FastMCP("mealie")
_force_mcp_loggers_to_stderr()  # MUST be after FastMCP constructor (Layer 2)

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
