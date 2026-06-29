<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import {required, WlkButton, WlkModalFooter, WlkTextInput} from "whelk-ui";
import {computed, ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {useDocumentationStore} from "@/stores/documentation/documentation.ts";
import type {DocumentItemInterface} from "@/utils/interfaces/documents/DocumentItemInterface.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		"en": {
			"cancel": "Cancel",
			"create_new_link": "Create new link",
			"description": "Description",
			"url": "Url Location",
		},
		"ja": {
			"cancel": "キャンセル",
			"create_new_link": "新しいリンクを作成する",
			"description": "説明",
			"url": "URLの場所",
		},
	}
});

// Define emits
const emit = defineEmits(["closeModal"]);

// Define object store
const documentationStore = useDocumentationStore();
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
	// TODO - add to optimistic list
	// TODO - close modal

	const parent_folder_id = documentationStore.currentFolderId === 0 ? null : documentationStore.currentFolderId;

	const body = {
		description: descriptionModel.value,
		type: "link",
		url_location: newLinkModel.value,
		parent_folder_id: parent_folder_id,
	}

	// TODO - clean models

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

		// TEMP CODE
		emit("closeModal");
		descriptionModel.value = "";
		newLinkModel.value = "";
		// END TEMP CODE
	} catch (error) {
		// TODO - Handle errors
		// TODO - Remove from optimistic list
	}
}

</script>

<template>
	<WlkTextInput class="compact"
				  placeholder="https://nearbeach.org/"
				  :label="t('url')"
				  :validationRules="[required()]"
				  v-model="newLinkModel"
	/>
	<WlkTextInput class="compact"
				  :label="t('description')"
				  v-model="descriptionModel"
    />

	<WlkModalFooter class="new-link-footer">
		<WlkButton
			class="compact"
			v-on:click="emit('closeModal')"
		>
			{{t("cancel")}}
		</WlkButton>
		<WlkButton
			class="compact primary"
			:disabled="isCreateDisabled"
			v-on:click="createNewLink"
		>
			{{t("create_new_link")}}
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