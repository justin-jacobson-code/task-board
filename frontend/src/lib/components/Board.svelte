<script lang="ts">
    import { flip } from "svelte/animate";
    import Column from "../components/Column.svelte";
    import type { ColumnData } from "$lib/types";
    const flipDurationMs = 300;

    export let columns: ColumnData[];

</script>

<section class="board" >
    {#each columns as {oid, name, items}, idx (oid)}
  		<div class="column" animate:flip="{{duration: flipDurationMs}}" >
            <Column name={name} items={items} />
        </div>
    {/each}
</section>