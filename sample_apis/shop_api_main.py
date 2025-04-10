# Import necessary modules from FastAPI and Pydantic.
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field
from typing import Optional, List

# -----------------------------------------------------------------------------
# Initialize FastAPI Application with Fake Store Metadata
# -----------------------------------------------------------------------------
app = FastAPI(
    title="Fake Store API",
    description=(
        "This API simulates a fake store experience. It offers endpoints to "
        "list available store items and to purchase a specific item. The detailed "
        "metadata is tailored for LLM agentic orchestration through semantic Swagger docs."
    ),
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Data Model Definitions with Enhanced Metadata
# -----------------------------------------------------------------------------
# StoreItem: Represents a product in the fake store.
class StoreItem(BaseModel):
    id: int = Field(
        ...,
        title="Product ID",
        description="A unique identifier for the store product."
    )
    name: str = Field(
        ...,
        title="Product Name",
        description="The name of the product."
    )
    description: Optional[str] = Field(
        None,
        title="Product Description",
        description="Detailed description of the product, including its features."
    )
    price: float = Field(
        ...,
        title="Product Price",
        description="The selling price of the product."
    )
    tax: Optional[float] = Field(
        None,
        title="Applicable Tax",
        description="Optional tax applied to the product's price."
    )

# PurchaseOrder: Represents an order to purchase a store item.
class PurchaseOrder(BaseModel):
    product_id: int = Field(
        ...,
        title="Product ID",
        description="The unique identifier of the product to purchase."
    )
    buyer_name: str = Field(
        ...,
        title="Buyer Name",
        description="The name of the customer placing the order."
    )
    quantity: int = Field(
        1,
        title="Quantity",
        description="The number of units to purchase. Defaults to 1."
    )

# -----------------------------------------------------------------------------
# In-Memory Fake Inventory (Simulated Database)
# -----------------------------------------------------------------------------
store_inventory = [
    StoreItem(
        id=1,
        name="Surface Laptop",
        description="A sleek Microsoft laptop with an elegant design and robust performance.",
        price=999.99,
        tax=99.99
    ),
    StoreItem(
        id=2,
        name="Wireless Mouse",
        description="An ergonomic wireless mouse with long battery life.",
        price=49.99,
        tax=4.99
    ),

    StoreItem(
        id=3,
        name="Pizza",
        description="A tasteful argentinian style pizza.",
        price=9.99,
        tax=1.99
    ),

    StoreItem(
        id=4,
        name="Frico",
        description="Delicacy from Udine.",
        price=9.99,
        tax=1.99
    )

    # Additional fake items can be added here.
]

# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

# GET Endpoint: List Store Items
@app.get(
    "/store/items",
    response_model=List[StoreItem],
    summary="List Store Items",
    description=(
        "Retrieve a list of all available items in the fake store. "
        "Each item includes its unique ID, name, description, price, and applicable tax."
    )
)
async def list_store_items():
    """
    List Store Items

    **Returns:**
    - A list of store items as JSON objects, each with:
      - *id*: Unique product identifier.
      - *name*: The product name.
      - *description*: Detailed product description.
      - *price*: The selling price.
      - *tax*: Applicable tax (if any).
    """
    return store_inventory

# POST Endpoint: Purchase an Item
@app.post(
    "/store/buy",
    summary="Purchase an Item",
    description=(
        "Place a purchase order for a specific store item. Provide the product ID, "
        "buyer name, and desired quantity. On successful processing, the endpoint returns "
        "an order confirmation with detailed purchase information."
    )
)
async def purchase_item(order: PurchaseOrder):
    """
    Purchase an Item

    **Parameters:**
    - **order**: A JSON object conforming to the PurchaseOrder model, including:
        - *product_id*: The unique identifier of the product.
        - *buyer_name*: The customer's name.
        - *quantity*: The number of units to purchase (defaults to 1).

    **Returns:**
    - A confirmation message containing:
        - The ordered product details.
        - The quantity purchased.
        - The calculated total price (product price plus applicable tax multiplied by the quantity).
    """
    # Locate the product in the fake inventory.
    product = next((item for item in store_inventory if item.id == order.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {order.product_id} not found.")

    # Calculate the total cost for the order.
    total_price = (product.price * order.quantity) + ((product.tax or 0) * order.quantity)

    order_confirmation = {
        "message": f"Thank you {order.buyer_name} for your purchase!",
        "product": product,
        "quantity": order.quantity,
        "total_price": total_price
    }
    return order_confirmation

# -----------------------------------------------------------------------------
# Custom OpenAPI Schema Function with Server Information
# -----------------------------------------------------------------------------
def custom_openapi():
    """
    Generate a custom OpenAPI schema with additional server information.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Add server information (e.g., for local development).
    openapi_schema["servers"] = [
        {"url": "http://127.0.0.1:8000", "description": "Local development server"}
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Override FastAPI's default OpenAPI schema generation.
app.openapi = custom_openapi
