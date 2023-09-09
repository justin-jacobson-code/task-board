<script lang="ts">
  import Board from "../components/Board.svelte";
  import type { ColumnData } from "../types/types";

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
</script>

<!-- Render the Board component -->
<Board columns={columnsData} />

