<script lang="ts">
	import { flip } from "svelte/animate";
	import { dndzone } from "svelte-dnd-action";
	import type { Item, Items } from "../types/types";
	import CardAddition from "./CardAddition.svelte";
	import Card from "./Card.svelte";
	const flipDurationMs = 150;

	export let name: string;
	export let items: Items;
	export let onDrop: (newItems: Items) => void;

	function handleDndConsiderCards(e: CustomEvent<{ items: any[] }>) {
		items = e.detail.items;
	}

	function handleDndFinalizeCards(e: CustomEvent<{ items: any[] }>) {
		onDrop(e.detail.items);
	}

	function deleteItem(itemToDelete: Item) {
		// filter out itemToDelete from items
		items = items.filter((item) => item.id !== itemToDelete.id);
	}
</script>

<div class="wrapper">
	<div class="column-title">
		{name}
	</div>
		<CardAddition bind:items />
	<div
		class="column-content"
		use:dndzone={{
			items,
			flipDurationMs,
			zoneTabIndex: -1,
			dropTargetStyle: {},
		}}
		on:consider={handleDndConsiderCards}
		on:finalize={handleDndFinalizeCards}
	>
		{#each items as item (item.id)}
			<Card bind:item={item} deleteItem={() => deleteItem(item)} />
		{/each}
	</div>
</div>

<style>
	@import "../styles.css";
</style>
