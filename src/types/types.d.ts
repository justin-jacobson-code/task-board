export type Item = { _id: number; name: string; };
export type Items = Array<Item>;

export type ColumnData = {
  _id: string;
  name: string;
  items: Items;
};

export let deleteItem: (item: Items) => void;