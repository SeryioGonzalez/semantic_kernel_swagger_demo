# Import necessary modules from FastAPI and Pydantic.
from fastapi import FastAPI, Path
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional, List

# -----------------------------------------------------------------------------
# Initialize FastAPI Application
# -----------------------------------------------------------------------------
# The FastAPI instance is configured with title, version, and a detailed description.
# This metadata appears in the generated Swagger docs.
app = FastAPI(
    title="Demo API",
    description=(
        "This API demonstrates how to create and document endpoints with detailed "
        "Swagger docs. Endpoints include item creation, retrieval, and listing all available items. "
        "This rich metadata is designed for LLM agentic frameworks or similar systems."
    ),
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Data Model Definition with Detailed Metadata
# -----------------------------------------------------------------------------
# The Item class defines the data model using Pydantic.
# Each field now includes titles and descriptions for enhanced Swagger documentation.
class Item(BaseModel):
    name: str = Field(
        ...,
        title="Item Name",
        description="The unique name of the item."
    )
    description: Optional[str] = Field(
        None,
        title="Item Description",
        description="A brief overview of the item, detailing its characteristics or purpose."
    )
    price: float = Field(
        ...,
        title="Item Price",
        description="The selling price of the item."
    )
    tax: Optional[float] = Field(
        None,
        title="Item Tax",
        description="The applicable tax for the item, if any."
    )

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

# POST Endpoint: Create an Item
# -----------------------------------------------------------------------------
# This endpoint accepts an item payload, validates it against the Item model,
# and returns the created item as confirmation.
@app.post(
    "/items/",
    response_model=Item,
    summary="Create an Item",
    description=(
        "Endpoint to create a new item. Provide detailed item information including its "
        "name, description, price, and optional tax. The endpoint returns the created item data."
    )
)
async def create_item(item: Item):
    """
    Create an Item

    **Parameters:**
    - **item**: A JSON object conforming to the Item model, including:
        - *name*: The item's unique name.
        - *description*: A brief description (optional).
        - *price*: The selling price.
        - *tax*: The applicable tax (optional).

    **Returns:**
    - The created item object, confirming the data received.
    """
    return item

# GET Endpoint: List All Available Items
# -----------------------------------------------------------------------------
# This endpoint retrieves a list of all available items. For demonstration, it returns
# a static list containing an example "Surface Laptop" as well as any additional items.
@app.get(
    "/items/",
    response_model=List[Item],
    summary="List All Items",
    description=(
        "Endpoint to retrieve a list of all available items. It returns each item with details "
        "such as name, description, price, and tax. For this demo, a fake list of items is provided "
        "that includes a 'Surface Laptop'."
    )
)
async def list_items():
    """
    List All Items

    **Returns:**
    - A list of items as JSON objects, each including:
        - *name*: The item name.
        - *description*: A description of the item.
        - *price*: The selling price.
        - *tax*: The applicable tax.
    """
    items = [
        Item(
            name="Surface Laptop",
            description="A sleek Microsoft laptop with an elegant design and robust performance.",
            price=999.99,
            tax=99.99
        ),
        # Add additional fake items here if necessary.
    ]
    return items

# GET Endpoint: Retrieve a Single Item by ID
# -----------------------------------------------------------------------------
# This endpoint demonstrates item retrieval by its unique identifier.
# For demonstration purposes, it returns a static item.
@app.get(
    "/items/{item_id}",
    response_model=Item,
    summary="Retrieve an Item",
    description=(
        "Endpoint to retrieve a specific item by its unique identifier. For demo purposes, "
        "a static item with predefined details is returned."
    )
)
async def read_item(
    item_id: int = Path(
        ...,
        title="Item ID",
        description="A unique integer identifier for the requested item."
    )
):
    """
    Retrieve an Item

    **Parameters:**
    - **item_id**: A unique integer identifying the item.

    **Returns:**
    - A JSON object representing the item, including:
        - *name*: The name of the item.
        - *description*: A brief description.
        - *price*: The selling price.
        - *tax*: The applicable tax.
    """
    return Item(name="Sample", price=100, description="Example item", tax=10)

# -----------------------------------------------------------------------------
# Custom OpenAPI Schema Function with Server Information
# -----------------------------------------------------------------------------
# FastAPI does not include the 'servers' field by default. This function generates
# a custom OpenAPI schema that injects server information to define the API's base URL.
def custom_openapi():
    """
    Generate a custom OpenAPI schema with additional server information.

    This function checks if an OpenAPI schema already exists. If not, it creates one using FastAPI's
    'get_openapi' utility and adds a 'servers' entry that defines the base URL for API access.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add server information, e.g., for local development.
    openapi_schema["servers"] = [
        {"url": "http://127.0.0.1:8000", "description": "Local development server"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override the default OpenAPI generation with the custom function.
app.openapi = custom_openapi
