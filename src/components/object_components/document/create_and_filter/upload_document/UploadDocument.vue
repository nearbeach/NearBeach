<script setup>
import {computed, ref} from 'vue'
import {WlkButton, WlkFileUpload, WlkModalFooter, WlkTextInput} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		"en": {
			"cancel": "Cancel",
			"document_name": "Document Name",
			"upload_document": "Upload Document",
		},
		"ja": {
			"cancel": "キャンセル",
			"document_name": "文書名",
			"upload_document": "ドキュメントをアップロード",
		},
	}
});

// Define stores
const documentationStore = useDocumentationStore();
const objectStore = useObjectStore();

// Define emits
const emit = defineEmits(["closeModal"]);

// Define refs
const documentModel = ref();
const documentNameModel = ref("");

// Define computed
const isUploadDisabled = computed(() => {
	// Two conditions;
	// 1. Document Model has to have documents within it
	// 2. Document Name Model has to have a value
	return !documentModel?.value?.length > 0 || !documentNameModel?.value?.length > 0;
})

// Define functions
function documentChanged() {
	for (const document of documentModel.value) {
		documentNameModel.value = document?.name;
	}
}

async function uploadDocument() {
	// Setup form data
	const body = new FormData();
	body.set("type", "document");
	body.set("description", documentNameModel.value);
	for (const document of documentModel.value) {
		body.append("document", document);
	}

	if (documentationStore.currentFolderId !== 0) {
		body.set("parent_folder_id", documentationStore.currentFolderId);
	}

	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/documents/`,
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
				body: body,
			},
		)

		const data = await response.json();
		// TODO - Fix this
		// const link: DocumentItemInterface = {
		// 	description: data.description.toString(),
		// 	key: data.key.toString(),
		// 	parent_folder_id: parseInt(data.parent_folder_id),
		// 	url_location: data.url_location.toString(),
		// 	document: data.document,
		// 	folder: null,
		// }
		// documentationStore.documents.push(link);

		// TEMP CODE
		emit("closeModal");
		// END TEMP CODE
	} catch (error) {
		console.log("ERROR: ", error);
		// TODO - Handle errors
		// TODO - Remove from optimistic list
	}
}
</script>

<template>
	<WlkFileUpload class="compact"
	               :label="t('upload_document')"
	               v-model="documentModel"
	               @change="documentChanged"
	/>

	<WlkTextInput class="compact"
	              :label="t('document_name')"
	              v-model="documentNameModel"
	/>
	<WlkModalFooter class="upload-document-footer">
		<WlkButton
			class="compact"
			v-on:click="emit('closeModal')"
		>
			{{ t("cancel") }}
		</WlkButton>
		<WlkButton
			class="compact primary"
			:disabled="isUploadDisabled"
			v-on:click="uploadDocument()"
		>
			{{ t("upload_document") }}
		</WlkButton>
	</WlkModalFooter>
</template>

<style scoped>
.upload-document-footer {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	padding-top: 1rem;
	margin-top: 0;
}
</style>