import type { UserData, Items } from "$lib/types";
import axios from "axios";

export async function getCardsFromDatabase(): Promise<UserData[]> {
    // call the API
    const res = await axios.get('http://0.0.0.0:80/items');
    let data = await res.data;

    console.log("Data: ", data);

    return data;
}

export async function updateColumnInDatabase(objectId: string, columnName: string, newItemsOrder: Items) {
    try {
        const response = await axios.put("http://0.0.0.0:80/items/update", {
            objectId,
            columnName,
            newItemsOrder,
        });

        if (response.status === 200) {
            console.log("Data updated successfully");
        } else {
            console.error("Failed to update data");
        }

    } catch (error) {
        console.error("Error updating data", error);
    }
}

export async function createCardInDatabase(objectId: string, columnName: string, newItem: Item) {
    try {
        const response = await axios.put("http://0.0.0.0:80/items/insert", {
            objectId,
            columnName,
            newItem,
        });

        if (response.status === 200) {
            console.log("Data inserted successfully");
        } else {
            console.error("Failed to insert data");
        }

    } catch (error) {
        console.error("Error inserting data", error);
    }
}

export async function deleteCardInDatabase(objectId: string, columnName: string, itemId: number) {
    try {
        const response = await axios.delete("http://0.0.0.0:80/items", {
            data: {
                objectId,
                columnName,
                itemId,
            },
        });

        if (response.status === 200) {
            console.log("Data updated successfully");
        } else {
            console.error("Failed to update data");
        }

    } catch (error) {
        console.error("Error updating data", error);
    }
}