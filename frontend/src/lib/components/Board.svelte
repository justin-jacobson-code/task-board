<script lang="ts">
    import { flip } from "svelte/animate";
    import Column from "../components/Column.svelte";
    import type { ColumnData, UserData } from "$lib/types";
    const flipDurationMs = 300;

    export let userData: UserData[];
    const columns: ColumnData[] = userData[0].columns;
    const objectId = userData[0].oid;

</script>

<section class="board" >
    {#each columns as {id, name, items}, idx (id)}
  		<div class="column" animate:flip="{{duration: flipDurationMs}}" >
            <Column objectId={objectId} name={name} items={items} />
        </div>
    {/each}
</section>