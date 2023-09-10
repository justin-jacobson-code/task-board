<script lang="ts">
    import type { Items } from "$lib/types";

    export let items: Items;
    let newCardName = "";

    function addCard() {
        if (newCardName.trim() !== "") {
            // Trigger an event to add the new card to the column
            const newCard = { id: Date.now(), name: newCardName };
            items = [newCard, ...items];

            // Clear the input field
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
