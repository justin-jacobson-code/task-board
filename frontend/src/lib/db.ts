import type { ColumnData } from "$lib/types";

const uri: string = process.env.MONGODB_URI ?? '';

if (uri === '') {
    throw new Error('MONGODB_URI environment variable is not defined.');
}

export async function getCardsFromDatabase(): Promise<ColumnData[]> {
    // call the API
    const res = await fetch('http://0.0.0.0:80/items');
    const data = await res.json();
    console.log(data);

    return data;
}