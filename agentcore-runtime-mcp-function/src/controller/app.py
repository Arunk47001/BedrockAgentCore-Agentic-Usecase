# importing the libraries
from mcp.server.fastmcp import FastMCP
from applications.vector_retreival import retrieval


mcp = FastMCP(host="0.0.0.0", stateless_http=True)


@mcp.tool()
def retrieve_information(query: str) -> str:
    """Retrieve information based on documents in using vector retrieval"""
    try:
        response = retrieval(query=query)
        return response
    except Exception as e:
        return f"Error during retrieval: {e}"



