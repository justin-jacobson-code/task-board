<script lang="ts">
    import { flip } from "svelte/animate";
    import Column from "../components/Column.svelte";
    import type { ColumnData, Items } from "../types/types";
    const flipDurationMs = 300;

    export let columns: ColumnData[];

 	function handleItemFinalize(columnIdx: number, newItems: Items) {
		columns[columnIdx].items = newItems;
		columns = [...columns];
	}

</script>

<section class="board" >
    {#each columns as {id, name, items}, idx (id)}
  		<div class="column"animate:flip="{{duration: flipDurationMs}}" >
            <Column name={name} items={items} onDrop={(newItems) => handleItemFinalize(idx, newItems)} />
        </div>
    {/each}
</section>