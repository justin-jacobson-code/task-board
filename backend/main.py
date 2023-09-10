from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

load_dotenv()

# Create a FastAPI instance
app = FastAPI()

# Define CORS settings
origins = [
    "http://localhost:5173",  # Add the URL of your SvelteKit app here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods if needed
    allow_headers=["*"],  # You can specify specific HTTP headers if needed
)

# MongoDB connection settings
MONGO_URI = os.environ['MONGODB_URI']  # Replace with your MongoDB URI
DB_NAME = "chores"  # Replace with your database name
COLLECTION_NAME = "cards"  # Replace with your collection name

logging.basicConfig(level=logging.DEBUG)
# logging.debug(MONGO_URI)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Pydantic model for the item
class Items(BaseModel):
    oid: str
    name: str
    items: List[dict]

class InsertColumnRequest(BaseModel):
    cardName: str
    newItem: dict
    columnName: str

class UpdateColumnRequest(BaseModel):
    columnName: str
    newItemsOrder: List[dict]

# Get all items
@app.get("/items", response_model=List[Items])
async def read_items():
    items = list(collection.find())
    serialized_items = []
    for item in items:
        serialized_item = {
            "oid": str(item["_id"]),  # Convert ObjectId to string
            "name": item["name"],
            "items": item["items"]
        }
        serialized_items.append(serialized_item)

    logging.debug(f'Items: {serialized_items}')
    return serialized_items

@app.put("/items/insert")
async def create_item(request: InsertColumnRequest):
    try:
        # Get the data from the request
        card_name = request.cardName
        new_item = request.newItem
        column_name = request.columnName

        logging.info(f'Card name: {card_name}')
        logging.info(f'New item: {new_item}')

        # Ensure that column_name and new_item are not None before proceeding
        if not card_name or not new_item:
            raise HTTPException(status_code=422, detail="Invalid request data")

        # Find the document with the matching column name
        column_document = collection.find_one({"name": column_name})
        logging.debug(f'Column document: {column_document}')

        if column_document is None:
            raise HTTPException(status_code=404, detail="Column not found")

        # # Append the new item to the "items" list in the document
        column_document["items"].insert(0, new_item)

        # Update the document in the collection
        collection.update_one(
            {"name": column_name},
            {"$set": {"items": column_document["items"]}}
        )

        logging.debug(f'{column_name} inserted successfully')

        return {"message": "Item inserted successfully"}
    except Exception as e:
        logging.error(f'CREATING ITEM FAILED: {e}')
        return HTTPException(status_code=500, detail="Internal server error")


# Update an item by ID
@app.put("/items/update")
async def update_items(request: UpdateColumnRequest):
    try:
        # Get the data from the request
        column_name = request.columnName
        new_items_order = request.newItemsOrder

        collection.update_one({"name": column_name}, {"$set": {"items": new_items_order}})

        logging.debug(f'{column_name} updated successfully')
        return {"message": "Column updated successfully"}
    except Exception as e:
        logging.error(e)
        return HTTPException(status_code=500, detail="Internal server error")

# Delete an item by ID
@app.delete("/items", response_model=Items)
async def delete_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    collection.delete_one({"_id": item_id})
    return item
