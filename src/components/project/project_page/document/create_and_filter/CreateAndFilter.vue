<script setup lang="ts">
import { ref } from "vue";
import {Folder, Link2, UploadCloudIcon} from "lucide-vue-next";
import type {DropDownItemsInterface} from "@/utils/interfaces/DropDownItemsInterface.ts";
import DropDown from "@/components/prefab/drop_down/DropDown.vue";

// Define refs
const dropDownItems = ref<DropDownItemsInterface[]>([
	{ariaLabel: "Create a new folder", icon: Folder, label: "New Folder", trigger: "new_folder"},
	{ariaLabel: "Create a new hyperlink", icon: Link2, label: "New Link", trigger: "new_link"},
	{ariaLabel: "Upload a document", icon: UploadCloudIcon, label: "Upload Document", trigger: "upload_document"},
]);

</script>

<template>
	<div class="document-create-and-filter">
		<DropDown
			:drop-down-items="dropDownItems"
			label="Create"
		/>
		<div class="filter">
			<input type="text" aria-label="Filter documents" placeholder="Filter documents..."/>
		</div>
	</div>
</template>

<style scoped>
.document-create-and-filter {
	display: flex;
	flex-direction: row;
	margin-top: 2rem;

	> .filter {
		flex: 1;

		> input {
			height: 1.75rem;
			font-size: 0.75rem;
			line-height: 1rem;
			padding: 0.1rem 0.5rem;
			border: solid;
			border-width: var(--border-width);
			border-color: var(--border-muted);
			border-radius: var(--border-radius);
			margin: 0 0 0 0.25rem;
			width: calc(100% - 1.5rem);

			@media (--small-screen) {
				margin: 0 0 0 1rem;
				width: calc(100% - 2rem);
			}
		}
	}
}
</style>