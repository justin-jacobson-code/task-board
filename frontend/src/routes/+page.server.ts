import type { ColumnData } from "$lib/types";
import { error } from '@sveltejs/kit';
import { getCardsFromDatabase } from "$lib/db";

export async function load() {
    let columnsData: ColumnData[] = await getCardsFromDatabase();
    // console.log(columnsData)
    // let columnsData: ColumnData[] = [
    //     {
    //         oid: "c1",
    //         name: "TODO",
    //         items: [
    //             { id: 1, name: "item41" },
    //             { id: 2, name: "item42" },
    //         ],
    //     },
    //     {
    //         oid: "c2",
    //         name: "DOING",
    //         items: [
    //             { id: 10, name: "item50" },
    //             { id: 11, name: "item51" },
    //         ],
    //     },
    //     {
    //         oid: "c3",
    //         name: "DONE",
    //         items: [{ id: 13, name: "item52" }],
    //     },
    // ];

    if (columnsData) {
        return { columnsData };
    }

    throw error(404, 'Not found');
}