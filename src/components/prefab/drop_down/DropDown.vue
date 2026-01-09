<script setup lang="ts">
import {ref} from 'vue';
import {ArrowDown} from "lucide-vue-next";
import type {PropType} from "vue";
import type {DropDownItemsInterface} from "@/utils/interfaces/DropDownItemsInterface.ts";
import DropDownItem from "@/components/prefab/drop_down/drop_down_item/DropDownItem.vue";

// Define props
const props = defineProps({
	dropDownItems: {
		type: Array as PropType<DropDownItemsInterface[]>,
		required: true,
	},
	label: {
		type: String,
		required: true,
	},
});

// Define emits
const emits = defineEmits(["dropDownItemClicked"]);

// Define refs
const menuOpen = ref(false);

// Define methods
function dropDownMenuClicked() {
	menuOpen.value = !menuOpen.value;
}

function dropDownItemClicked(trigger: string) {
	// Emit upstream
	emits("dropDownItemClicked", trigger);

	// Close the menu
	menuOpen.value = false;
}
</script>

<template>
	<div class="drop-down">
		<button
			type="button"
			v-on:click="dropDownMenuClicked"
		>
			{{ label }}
			<ArrowDown aria-hidden="true"/>
		</button>
		<Transition>
			<DropDownItem
				v-show="menuOpen"
				v-on:dropDownItemClicked="dropDownItemClicked"
				:drop-down-items="dropDownItems"
			/>
		</Transition>
		<Transition>
			<div
				v-on:click="dropDownMenuClicked"
				v-if="menuOpen"
				class="drop-down-backdrop"
			></div>
		</Transition>
	</div>
</template>

<style scoped>
.drop-down {
	> button {
		border: solid;
		border-width: 1px;
		border-radius: var(--border-radius);
		border-color: var(--border-muted);
		background: var(--bg-light);
		box-shadow: none;
		font-size: 1rem;
		line-height: 1.25rem;
		height: 2rem;
		padding: 0 1rem;
		position: relative;
		z-index: 10;

		> svg {
			width: 1rem;
			height: 1rem;
			transform: translateY(2px);
		}
	}

	.drop-down-backdrop {
		width: 100vw;
		height: 100dvh;
		z-index: 5;
		background-color: hsla(0, 0%, 0%, 0.7);
		position: fixed;
		top: 0;
		left: 0;
	}
}

.v-enter-active,
.v-leave-active {
	transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
	opacity: 0;
}

</style>