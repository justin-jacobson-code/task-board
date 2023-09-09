<script lang="ts">
  import Board from "../components/Board.svelte";
  import type { PageData } from "./$types";
  export let data: PageData;
</script>

<!-- Render the Board component -->
<Board columns={data.columnsData} />