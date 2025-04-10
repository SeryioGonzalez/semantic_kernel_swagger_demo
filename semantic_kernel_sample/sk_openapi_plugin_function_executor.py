import asyncio
import semantic_kernel as sk
import logging

from semantic_kernel.functions.kernel_arguments import KernelArguments

# Get the OPEN_API_FILE path from command line
import sys
if len(sys.argv) > 1:
    OPENAPI_FILE = sys.argv[1]
else:
    sys.exit("Please provide the path to the OpenAPI file as a command line argument.")

logger = logging.getLogger(__name__)


async def main():
    """Client"""
    kernel = sk.Kernel()
    logging.info("Kernel loaded")

    openapi_plugin = kernel.add_plugin_from_openapi(plugin_name="openApiPlugin", openapi_document_path=OPENAPI_FILE)

    # Simulate a user interaction
    # These are the methods you would collect through an agentic interaction with the user
    arguments = {"name": "Laptop", "description": "High-end device", "price": 1500.0, "tax": 150.0}
    kernel_arguments = KernelArguments(**arguments)

    # Posting to the API explicitly
    # This is where you would call the plugin method
    result = await kernel.invoke(openapi_plugin["create_item_items__post"], arguments=kernel_arguments)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())