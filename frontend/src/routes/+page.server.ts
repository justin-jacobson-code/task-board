import type { UserData } from "$lib/types";
import { error } from '@sveltejs/kit';
import { getCardsFromDatabase } from "$lib/db";

export async function load() {
    let userData: UserData[] = await getCardsFromDatabase();
    // console.log(userData)

    if (userData) {
        return { userData };
    }

    throw error(404, 'Not found');
}