<script lang="ts">
    import type { Items } from "$lib/types";
    import { createCardInDatabase } from "$lib/db";

    export let items: Items;
    export let columnName: string;
    export let objectId: string;
    let newCardName = "";

    function addCard() {
        if (newCardName.trim() !== "") {
            const newItem = { id: Date.now(), taskName: newCardName };
            items = [newItem, ...items];
            createCardInDatabase(objectId, columnName, newItem);

            newCardName = "";
        }
    }

</script>

<div class="card-addition">
    <input
        type="text"
        placeholder="Enter Task"
        bind:value={newCardName}
        on:keydown={(event) => {
            if (event.key === "Enter") {
                addCard();
            }
        }}
    />
    <!-- <button on:click={addCard}>Add Card</button> -->
</div>
