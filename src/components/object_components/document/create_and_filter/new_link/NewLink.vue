<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import {required, WlkButton, WlkModalFooter, WlkTextInput} from "whelk-ui";
import {computed, ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";

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

	const body = {
		description: descriptionModel.value,
		type: "link",
		url_location: newLinkModel.value,
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
				body: JSON.stringify(body),
			},
		)

		const data = await response.json();
		emit("closeModal");
		// TODO - Update the folders in DocumentComponent
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