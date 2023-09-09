export type Items = Array<{ id: number; name: string; }>;

export type ColumnData = {
  id: string;
  name: string;
  items: Items;
};
