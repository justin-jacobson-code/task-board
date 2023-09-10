import os
import logging
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.environ['MONGODB_URI']
DB_NAME = "chores"
COLLECTION_NAME = "cards"

logging.basicConfig(level=logging.DEBUG)

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


class Items(BaseModel):
    oid: str
    name: str
    items: list[dict]


class InsertColumnRequest(BaseModel):
    columnName: str
    cardName: str
    newItem: dict


class UpdateColumnRequest(BaseModel):
    columnName: str
    newItemsOrder: list[dict]


@app.get("/items", response_model=list[Items])
async def read_items():
    """Get all items from the database and return serialized list"""
    try:
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

    except Exception as e:
        logging.error(e)
        return HTTPException(status_code=500, detail="Internal server error")


@app.put("/items/insert")
async def create_item(request: InsertColumnRequest):
    """Create a new item in column"""
    try:
        # Get the data from the request
        card_name = request.cardName
        new_item = request.newItem
        column_name = request.columnName

        logging.debug(f'Card name: {card_name}')
        logging.debug(f'New item: {new_item}')

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


@app.put("/items/update")
async def update_items(request: UpdateColumnRequest):
    """Update an item in column"""
    try:
        # Get the data from the request
        column_name = request.columnName
        new_items_order = request.newItemsOrder

        collection.update_one({"name": column_name}, {
                              "$set": {"items": new_items_order}})

        logging.debug(f'{column_name} updated successfully')
        return {"message": "Column updated successfully"}
    except Exception as e:
        logging.error(e)
        return HTTPException(status_code=500, detail="Internal server error")


@app.delete("/items", response_model=Items)
async def delete_item(item_id: str):
    item = collection.find_one({"_id": item_id})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    collection.delete_one({"_id": item_id})
    return item
