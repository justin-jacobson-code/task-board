export type Item = { id: number; name: string; };
export type Items = Array<Item>;

export type ColumnData = {
  id: string;
  name: string;
  items: Items;
};

export let deleteItem: (item: Items) => void;