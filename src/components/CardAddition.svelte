<script lang="ts">
	import type { Items } from "../types/types";

    export let items: Items;
    let newCardName = "";

    function addCard() {
      if (newCardName.trim() !== "") {
        // Trigger an event to add the new card to the column
        const newCard = { id: Date.now(), name: newCardName };
        items = [...items, newCard];

        // Clear the input field
        newCardName = "";
      }
    }
  </script>

  <div class="card-addition">
    <input
      type="text"
      placeholder="Enter card name"
      bind:value={newCardName}
    />
    <button on:click={addCard}>Add Card</button>
  </div>

  <style>
    /* Add styles for the card addition component */
    .card-addition {
      margin-top: 1em;
      display: flex;
    }
  </style>
