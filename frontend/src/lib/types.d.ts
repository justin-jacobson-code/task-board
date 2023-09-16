export type Item = { id: number; taskName: string; };
export type Items = Array<Item>;

export type ColumnData = {
  id: string;
  name: string;
  items: Items;
};

export type UserData = {
  oid: string;
  name: string;
  columns: ColumnData[];
}

export let deleteItem: (item: Items) => void;