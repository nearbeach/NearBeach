<script setup lang="ts">
import type {PropType} from "vue";
import type {DropDownItemsInterface} from "@/utils/interfaces/DropDownItemsInterface.ts";

// Define props
defineProps({
	dropDownItems: {
		type: Array as PropType<DropDownItemsInterface[]>,
		required: true,
	},
});

// Define emits
const emits = defineEmits(["dropDownItemClicked"]);

// Define methods
function dropDownItemClicked(trigger: string) {
	emits("dropDownItemClicked", trigger);
}
</script>

<template>
	<div class="drop-down-items">
		<div class="drop-down-item"
			 v-for="item in dropDownItems"
			 v-on:click="dropDownItemClicked(item.trigger)"
			 :key="item.label"
		>
			<component :is="item.icon" />
			{{item.label}}
		</div>
	</div>
</template>

<style scoped>
.drop-down-items {
	position: absolute;
	background-color: var(--bg-light);
	border: solid;
	border-width: var(--border-width);
	border-radius: var(--border-radius);
	border-color: var(--border-muted);
	z-index: 20;

	> .drop-down-item {
		padding: 0.25rem 0.5rem;

		&:hover {
			background-color: var(--bg-dark);
		}

		> svg {
			width: 0.75rem;
			height: 0.75rem;
		}
	}
}
</style>