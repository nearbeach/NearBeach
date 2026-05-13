<script setup lang="ts">
import type {FolderArrayInterface} from "@/utils/interfaces/documents/BreadCrumbsArrayInterface.ts";
import {computed, type PropType} from "vue";

// Define props
const props = defineProps({
	breadCrumbsArray: {
		type: Array as PropType<FolderArrayInterface[]>,
		required: true,
	},
});

// Define emits
const emits = defineEmits(["goToRootFolder","updateFolderLocation"]);

// Define computed
const currentFolderLabel = computed(() => {
	// If folderArray length is 0 - return null string
	if (props.breadCrumbsArray?.length === 0) {
		return "";
	}

	// Get last array object and return the label
	return props.breadCrumbsArray[props.breadCrumbsArray.length - 1]?.label;
});

const getInbetweenFolders = computed(() => {
	if (props.breadCrumbsArray?.length <= 1) {
		// Nothing to return
		return [];
	}

	return props.breadCrumbsArray.slice(0, props.breadCrumbsArray?.length - 1);
});
</script>

<template>
	<div class="bread-crumbs">
		<a
			type="button"
			class="root-button"
			v-on:click="emits('goToRootFolder')"
		>
			Root
		</a>
		<span class="middle-span">
			<a v-for="(folder, index) in getInbetweenFolders"
			   class="navigation-button"
			   type="button"
			   :key="folder.folderId"
			   v-on:click="emits('updateFolderLocation', { index })"
			>
				{{folder.label}}
			</a>
		</span>
		<span class="end-span">{{currentFolderLabel}}</span>
	</div>
</template>

<style scoped>
.bread-crumbs {
	display: flex;
	flex-direction: row;
	border-bottom: dashed;
	border-bottom-color: var(--border-muted);
	border-bottom-width: var(--border-width);
	padding: 1.5rem 0 0.5rem 0;
	font-weight: 100;
	font-family: "Roboto", sans-serif;

	> .root-button {
		text-decoration-color: var(--document-links);
		color: var(--document-links);

		&:after {
			content: "/";
		}
	}

	> .middle-span href="#"{
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		direction: rtl;

		> .navigation-button {
			text-decoration-color: var(--document-links);
			color: var(--document-links);

			&:after {
				content: "/";
			}

			&:last-child {
				&:after {
					content: "";
				}
			}
		}
	}

	> .end-span {
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		max-width: 50%;
	}
}

</style>