import type { ColumnData } from "../types/types";
import { error } from '@sveltejs/kit';
import { getCardsFromDatabase } from "$lib/db";

export async function load() {
    let columnsData: ColumnData[] = await getCardsFromDatabase();
    // let columnsData: ColumnData[] = [
    //     {
    //         _id: "c1",
    //         name: "TODO",
    //         items: [
    //             { _id: 1, name: "item41" },
    //             { _id: 2, name: "item42" },
    //         ],
    //     },
    //     {
    //         _id: "c2",
    //         name: "DOING",
    //         items: [
    //             { _id: 10, name: "item50" },
    //             { _id: 11, name: "item51" },
    //         ],
    //     },
    //     {
    //         _id: "c3",
    //         name: "DONE",
    //         items: [{ _id: 13, name: "item52" }],
    //     },
    // ];

    if (columnsData) {
        return { columnsData };
    }

    throw error(404, 'Not found');
}