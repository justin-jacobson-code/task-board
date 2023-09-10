import type { ColumnData } from "$lib/types";
import { MongoClient, Db, Collection } from 'mongodb';

const uri: string = process.env.MONGODB_URI ?? '';

if (uri === '') {
    throw new Error('MONGODB_URI environment variable is not defined.');
}

async function connectToMongo(): Promise<Db> {
    const client = new MongoClient(uri);

    try {
        await client.connect();
        console.log('Connected to MongoDB');
        return client.db('chores');
    } catch (error) {
        console.error('Error connecting to MongoDB', error);
        throw error;
    }
}

export async function getCardsFromDatabase(): Promise<ColumnData[]> {
    const db = await connectToMongo();
    const collection: Collection<ColumnData> = db.collection('cards');
    const documents: ColumnData[] = await collection.find().toArray();

    const serializedDocuments: ColumnData[] = documents.map((doc) => {
        return {
            ...doc,
            _id: doc._id.toString(),
        };
    });

    return serializedDocuments;
}