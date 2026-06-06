"""FastMCP Server for RootBrowse"""

from mcp.server.fastmcp import FastMCP
from .tools import register_tools


def main():
    mcp = FastMCP("RootBrowse")
    register_tools(mcp)
    mcp.run()


if __name__ == "__main__":
    main()