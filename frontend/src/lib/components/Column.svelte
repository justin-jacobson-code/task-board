<script lang="ts">
	import { dndzone } from "svelte-dnd-action";
	import type { Item, Items } from "$lib/types";
	import CardAddition from "./CardAddition.svelte";
	import Card from "./Card.svelte";
	import { deleteCardInDatabase, updateColumnInDatabase } from "$lib/db";

	const flipDurationMs = 220;
	export let name: string;
	export let items: Items;

	function handleDndCard(e: CustomEvent<{ items: Items }>) {
		items = e.detail.items;
		updateColumnInDatabase(name, items);
	}

	function deleteItem(itemToDelete: Item) {
		// filter out itemToDelete from items
		items = items.filter((item: Item) => item.id !== itemToDelete.id);
		// deleteCardInDatabase
	}

</script>

<div class="wrapper">
	<div class="column-title">
		{name}
	</div>
		<CardAddition bind:items columnName={name} />
	<div
		class="column-content"
		use:dndzone={{
			items,
			flipDurationMs,
			zoneTabIndex: -1,
			dropTargetStyle: {},
		}}
		on:consider={handleDndCard}
		on:finalize={handleDndCard}
	>
		{#each items as item (item.id)}
			<Card bind:item={item} deleteItem={(item) => deleteItem(item)} />
		{/each}
	</div>
</div>

<style>
	@import "../../styles.css";
</style>
