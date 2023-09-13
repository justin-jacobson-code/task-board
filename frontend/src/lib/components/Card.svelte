<script lang="ts">
    import type { Item } from "$lib/types";
    export let item: Item;
    export let deleteItem: (item: Item) => void;
</script>

<div class="card">
    <!-- Delete button -->
    <span
        class="delete-button"
        role="button"
        tabindex="0"
        aria-label="Delete"
        on:click={() => deleteItem(item)}
        on:keypress={(event) => {
            if (event.key === "Enter" || event.key === " ") {
                deleteItem(item);
            }
        }}
    >
        X
    </span>

    <!-- Card content -->
    {item.taskName}
</div>
