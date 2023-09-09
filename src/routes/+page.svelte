<script lang="ts">
  import Board from "../components/Board.svelte";
  export let data;
</script>

<!-- Render the Board component -->
<Board columns={data.columnsData} />