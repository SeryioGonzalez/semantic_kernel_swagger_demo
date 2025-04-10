import asyncio
import semantic_kernel as sk
import logging

from semantic_kernel.functions.kernel_arguments import KernelArguments


OPENAPI_FILE = "../fake_api/openapi.json"

logger = logging.getLogger(__name__)


async def main():
    """Client"""
    kernel = sk.Kernel()
    logging.info("Kernel loaded")

    openapi_plugin = kernel.add_plugin_from_openapi(plugin_name="openApiPlugin", openapi_document_path=OPENAPI_FILE)

    for function in openapi_plugin.functions:
        print(f"Function: {function}")
        print("-" * 40)

    import sys; sys.exit()


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