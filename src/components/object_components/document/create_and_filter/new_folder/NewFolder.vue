<script setup lang="ts">
import {WlkButton, required, WlkTextInput, WlkModalFooter} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {computed, ref} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import type {FolderItemInterface} from "@/utils/interfaces/documents/FolderItemInterface.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		"en": {
			"cancel": "Cancel",
			"create_new_folder": "Create new folder",
			"new_folder_name": "New Folder Name",
			"new_folder_placeholder": "Statistics Folder",
		},
		"ja": {
			"cancel": "キャンセル",
			"create_new_folder": "新しいフォルダーを作成する",
			"new_folder_name": "新しいフォルダ名",
			"new_folder_placeholder": "統計フォルダ",
		}
	}
});

// Define store
const documentationStore = useDocumentationStore();

// Define emits
const emit = defineEmits(["closeModal"]);

// Define object store
const objectStore = useObjectStore();

// Define refs
const newFolderModel = ref<string>("")

// Define computed component
const isCreateDisabled = computed(() => {
	if (newFolderModel.value === "") {
		// Disable the button
		return true;
	}
	// TODO - check the if the folder name already exists in the current folder
});

// Define functions
async function createNewFolder() {
	// TODO - add to optimistic list
	// TODO - close modal

	const body = {
		description: newFolderModel.value,
		type: "folder",
		parent_folder_id: documentationStore.currentFolderId === 0
			? null
			: documentationStore.currentFolderId,
	}

	// TODO - clear data from models

	try {
		const response = await fetch(
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

		// Add data
		const data = await response.json();
		const folder: FolderItemInterface = {
			id: data.id,
			description: data.description,
			parent_folder_id: data.parent_folder_id,
		}
		documentationStore.folders.push(folder);

		// TEMP CODE
		emit("closeModal");
		newFolderModel.value = "";
		// END TEMP CODE

		// TODO - Update the folders in DocumentComponent
	} catch (error) {
		// TODO - Handle errors
		// TODO - Remove from optimistic list
	}
}

</script>

<template>
	<WlkTextInput class="compact"
	              :label="t('new_folder_name')"
	              :placeholderText="t('new_folder_placeholder')"
	              :validationRules="[required()]"
	              v-model="newFolderModel"
	/>
	<WlkModalFooter class="new-folder-footer">
		<WlkButton
			class="compact"
			v-on:click="emit('closeModal')"
		>
			{{ t("cancel") }}
		</WlkButton>
		<WlkButton
			class="compact primary"
			:disabled="isCreateDisabled"
			v-on:click="createNewFolder"
		>
			{{ t("create_new_folder") }}
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