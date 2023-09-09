<script lang="ts">
    import { flip } from "svelte/animate";
    import Column from "../components/Column.svelte";
    import type { ColumnData } from "../types/types";
    const flipDurationMs = 300;

    export let columns: ColumnData[];

</script>

<section class="board" >
    {#each columns as {id, name, items}, idx (id)}
  		<div class="column"animate:flip="{{duration: flipDurationMs}}" >
            <Column name={name} items={items} />
        </div>
    {/each}
</section>