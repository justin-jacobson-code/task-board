import type { ColumnData, Items } from "$lib/types";
import axios from "axios";

export async function getCardsFromDatabase(): Promise<ColumnData[]> {
    // call the API
    const res = await axios.get('http://0.0.0.0:80/items');
    const data = await res.data;
    console.log("Data: ", data);

    return data;
}

export async function updateColumnInDatabase(columnName: string, newItemsOrder: Items) {
    try {
        const response = await axios.put("http://0.0.0.0:80/items/update", {
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

export async function createCardInDatabase(columnName: string, cardName: string, newItem: Item) {
    try {
        const response = await axios.put("http://0.0.0.0:80/items/insert", {
            columnName,
            cardName,
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

export async function deleteCardInDatabase(columnName: string, newItemsOrder: Items) {
    try {
        const response = await axios.delete("http://0.0.0.0:80/items", {
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