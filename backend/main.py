from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Create a FastAPI instance
app = FastAPI()

# MongoDB connection settings
MONGO_URI = os.environ['MONGODB_URI']  # Replace with your MongoDB URI
DB_NAME = "chores"  # Replace with your database name
COLLECTION_NAME = "cards"  # Replace with your collection name

logging.basicConfig(level=logging.DEBUG)
logging.debug(MONGO_URI)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Pydantic model for the item
class Item(BaseModel):
    oid: str
    name: str
    items: List[dict]

# Get all items
@app.get("/items", response_model=List[Item])
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

# Create an item
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    inserted_item = collection.insert_one(item.dict())
    item.id = str(inserted_item.inserted_id)
    return item

# Get a single item by ID
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update an item by ID
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    updated_item = collection.update_one({"_id": item_id}, {"$set": item.dict()})
    if updated_item.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Delete an item by ID
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    collection.delete_one({"_id": item_id})
    return item
