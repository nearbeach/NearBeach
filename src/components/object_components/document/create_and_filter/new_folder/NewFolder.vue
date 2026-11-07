<script setup lang="ts">
import {WlkButton, required, WlkTextInput, WlkModalFooter} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {computed, ref} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define i18n
const {t} = useI18n();

// Define store
const documentationStore = useDocumentationStore();
const errorStore = useErrorStore();

// Define emits
const emit = defineEmits(["closeModal"]);

// Define object store
const objectStore = useObjectStore();

// Define refs
const newFolderModel = ref<string>("")

// Define computed component
const isCreateDisabled = computed((): boolean => {
	if (newFolderModel.value === "") {
		// Disable the button
		return true;
	}

	return documentationStore.folders.some((folder: FolderItemInterface) => {
		const condition_1 = folder.description.toLowerCase() === newFolderModel.value.toLowerCase();
		const condition_2 = folder.parent_folder_id === documentationStore.currentFolderId;

		return condition_1 && condition_2;
	});
});

// Define functions
async function createNewFolder() {
	const body = {
		description: newFolderModel.value,
		type: "folder",
		parent_folder_id: documentationStore.currentFolderId === 0
			? null
			: documentationStore.currentFolderId,
	}

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/documents/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		},
	)

	// Close the modal
	emit("closeModal");

	switch (response.status) {
		case 201:
			const data = await response.json();
			const folder: FolderItemInterface = {
				id: data.id,
				description: data.description,
				parent_folder_id: data.parent_folder_id,
			}
			documentationStore.folders.push(folder);

			// Clear the model
			newFolderModel.value = "";
			break;
		case 403:
			errorStore.setError(t("general_detail_component.error_forbidden"));
			errorStore.showErrorModal = true;
			break;
		default:
			errorStore.setError(response.statusText);
			errorStore.showErrorModal = true;
			break;
	}
}
</script>

<template>
	<WlkTextInput class="compact"
	              :label="t('new_folder.new_folder_name')"
	              :placeholderText="t('new_folder.new_folder_placeholder')"
	              :validationRules="[required()]"
	              v-model="newFolderModel"
	/>
	<WlkModalFooter class="new-folder-footer">
		<WlkButton
			class="compact"
			v-on:click="emit('closeModal')"
		>
			{{ t("new_folder.cancel") }}
		</WlkButton>
		<WlkButton
			class="compact primary"
			:disabled="isCreateDisabled"
			v-on:click="createNewFolder"
		>
			{{ t("new_folder.create_new_folder") }}
		</WlkButton>
	</WlkModalFooter>
</template>

<style scoped>
.new-folder-footer {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	padding-top: 1rem;
	margin-top: 0;
}

</style>