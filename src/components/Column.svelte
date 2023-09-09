<script lang="ts">
	import { flip } from "svelte/animate";
	import { dndzone } from "svelte-dnd-action";
	import type { Items } from "../types/types";
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

</script>

<div class="wrapper">
	<div class="column-title">
		{name}
	</div>
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

		{#each items as item (item)}
			<div class="card" animate:flip={{ duration: flipDurationMs }}>
				{item.name}
			</div>
		{/each}

	</div>
</div>

<style>
	@import "../styles.css";
</style>
