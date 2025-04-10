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
OPENAPI_FILE = "../sample_apis/fake_openapi.json"
SERVICE_ID = "az_openai_chat_gpt4o"
USER_INPUT = "I want to know which products are available in the store."

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
    openapi_plugin = kernel.add_plugin_from_openapi(plugin_name="openApiPlugin", openapi_document_path=OPENAPI_FILE)


    print("Create a chat history collection")
    history = ChatHistory()
    history.add_user_message(USER_INPUT)

    print("Enable planning")
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()


    result = await chat_completion.get_chat_message_content(
    chat_history=history,
    settings=execution_settings,
    kernel=kernel,
    )

    # Print the results
    print("Assistant > " + str(result))

# Add the message from the agent to the chat history
    history.add_message(result)
    

if __name__ == "__main__":
    asyncio.run(main())