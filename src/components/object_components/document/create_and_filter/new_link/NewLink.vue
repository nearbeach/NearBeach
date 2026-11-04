<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import {required, WlkButton, WlkModalFooter, WlkTextInput} from "whelk-ui";
import {computed, ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import type {DocumentItemInterface} from "@/utils/interfaces/documents/DocumentItemInterface.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define i18n
const {t} = useI18n();

// Define emits
const emit = defineEmits(["closeModal"]);

// Define object store
const documentationStore = useDocumentationStore();
const errorStore = useErrorStore();
const objectStore = useObjectStore();

// Define refs
const descriptionModel = ref("");
const newLinkModel = ref("");

// Define computed
const isCreateDisabled = computed(() => {
	return newLinkModel.value === "";
})

// Define function
async function createNewLink() {
	// Define parent folder id
	const parent_folder_id = documentationStore.currentFolderId === 0 ? null : documentationStore.currentFolderId;

	// Create the body
	const body = {
		description: descriptionModel.value,
		type: "link",
		url_location: newLinkModel.value,
		parent_folder_id,
	}

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

	// Close modal
	emit("closeModal");

	switch (response.status) {
		case 201:
			const data = await response.json();
			const link: DocumentItemInterface = {
				description: data.description.toString(),
				key: data.key.toString(),
				parent_folder_id: parseInt(data.parent_folder_id),
				url_location: data.url_location.toString(),
				document: null,
				folder: null,
			}
			documentationStore.documents.push(link);

			// Clear the model data
			descriptionModel.value = "";
			newLinkModel.value = "";
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
	              placeholder="https://nearbeach.org/"
	              :label="t('new_link.url')"
	              :validationRules="[required()]"
	              v-model="newLinkModel"
	/>
	<WlkTextInput class="compact"
	              :label="t('new_link.description')"
	              v-model="descriptionModel"
	/>

	<WlkModalFooter class="new-link-footer">
		<WlkButton
			class="compact"
			v-on:click="emit('closeModal')"
		>
			{{ t("new_link.cancel") }}
		</WlkButton>
		<WlkButton
			class="compact primary"
			:disabled="isCreateDisabled"
			v-on:click="createNewLink"
		>
			{{ t("new_link.create_new_link") }}
		</WlkButton>
	</WlkModalFooter>
</template>

<style scoped>
.new-link-footer {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	padding-top: 1rem;
	margin-top: 0;
}
</style>