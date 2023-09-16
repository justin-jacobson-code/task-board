<script lang="ts">
  import Board from "$lib/components/Board.svelte";
  import type { PageData } from "./$types";
  export let data: PageData;
</script>

<!-- Render the Board component -->
<h1>Task Board</h1>
<Board userData={data.userData} />

<style>
  @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
</style>