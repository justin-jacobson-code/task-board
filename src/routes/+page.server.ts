import type { ColumnData } from "../types/types";
import { error } from '@sveltejs/kit';

/** @type {import('./$types').PageServerLoad} */
export async function load() {
    // const post = await getPostFromDatabase(params.slug);
    let columnsData: ColumnData[] = [
        {
            id: "c1",
            name: "TODO",
            items: [
                { id: 1, name: "item41" },
                { id: 2, name: "item42" },
            ],
        },
        {
            id: "c2",
            name: "DOING",
            items: [
                { id: 10, name: "item50" },
                { id: 11, name: "item51" },
            ],
        },
        {
            id: "c3",
            name: "DONE",
            items: [{ id: 13, name: "item52" }],
        },
    ];

    if (columnsData) {
        return { columnsData };
    }

    throw error(404, 'Not found');
}