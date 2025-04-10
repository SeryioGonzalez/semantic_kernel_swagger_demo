import asyncio
import semantic_kernel as sk

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.function_choice_behavior import (
    FunctionChoiceBehavior,
)

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)



AZURE_OPENAI_DEPLOYMENT = "gpt-4o-2024-11-20"
OPENAPI_FILE = "../sample_apis/shop_openapi.json"
SERVICE_ID = "az_openai_chat_gpt4o"

SYSTEM_MESSAGE = """
You are a helpful assistant that can answer questions about the products available in the store.
Limit yourself to questions related to the store.
If the user asks about something else, please inform them that you can only answer questions related to the store.
"""

async def main():
    """Client"""
    print("Starting agent")
    
    kernel = sk.Kernel()
    print("Kernel loaded")

    print("Loading AzOpenAI service to kernel") 
    chat_completion = AzureChatCompletion(
            service_id=SERVICE_ID,
            deployment_name=AZURE_OPENAI_DEPLOYMENT
        )

    kernel.add_service(chat_completion)

    print("Loading OpenAPI plugin to kernel")
    _ = kernel.add_plugin_from_openapi(plugin_name="openApiPlugin", openapi_document_path=OPENAPI_FILE)

    print("Create a chat history collection")

    history = ChatHistory(system_message=SYSTEM_MESSAGE)
    
    print("Enable planning")
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()




    # Start an interactive loop
    while True:
        # Get input from the user
        user_input = input("User > ")
        # Provide a mechanism to exit the loop
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        # Add the user's message to the chat history
        history.add_user_message(user_input)

        # Get the assistant's response using the chat completion service
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the assistant's answer to the console
        print("Assistant > " + str(result))

        # Optionally, you could store the assistant's answer in the history:
        history.add_assistant_message(str(result))
    

if __name__ == "__main__":
    asyncio.run(main())