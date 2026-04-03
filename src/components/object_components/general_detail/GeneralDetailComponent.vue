<script setup lang="ts">
import {onMounted, inject, ref, computed} from 'vue';
import {maxLength, minLength, required, WlkButton, WlkCard, WlkCardHeader, WlkTextArea, WlkTextInput} from 'whelk-ui';
import type {AxiosInstance} from "axios";
import {useObjectStore} from "@/stores/object/object.ts";
import {useRoute} from "vue-router";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			_details: "Project Details",
			_sub_text: "Update and modify your project details",
			_title_placeholder: "Your project title",
			_description_placeholder: "Description of your project",
			project_details: "Project Details",
			project_sub_text: "Update and modify your project details",
			project_title_placeholder: "Your project title",
			project_description_placeholder: "Description of your project",
			requirement_details: "Requirement Details",
			requirement_sub_text: "Update and modify your requirement details",
			requirement_title_placeholder: "Your requirement title",
			requirement_description_placeholder: "Description of your requirements",
			requirement_item_details: "Requirement Item Details",
			requirement_item_sub_text: "Update and modify your requirement item details",
			requirement_item_title_placeholder: "Your requirement item title",
			requirement_item_description_placeholder: "Description of your requirement item",
			task_details: "Task Details",
			task_sub_text: "Update and modify your task details",
			task_title_placeholder: "Your task title",
			task_description_placeholder: "Description of your task",
			title: "Title",
			description: "Description",
			update: "Update description and title",
			update_error: "There was a problem updating",
			updated: "Your updates have been processed",
			updating: "Please wait",
		},
		ja: {
			project_details: "プロジェクトの詳細",
			project_sub_text: "プロジェクトの詳細を更新および変更する",
			project_title_placeholder: "プロジェクトタイトル",
			project_description_placeholder: "プロジェクトの説明",
			requirement_details: "要件の詳細",
			requirement_sub_text: "要件の詳細を更新および変更します",
			requirement_title_placeholder: "要件のタイトル",
			requirement_description_placeholder: "ご要望の説明",
			requirement_item_details: "必要品目の詳細",
			requirement_item_sub_text: "必要品目の詳細を更新および変更します",
			requirement_item_title_placeholder: "要件アイテムのタイトル",
			requirement_item_description_placeholder: "ご要望の品目についての説明",
			task_details: "タスクの詳細",
			task_sub_text: "タスクの詳細を更新および変更します",
			task_title_placeholder: "あなたのタスクタイトル",
			task_description_placeholder: "業務内容の説明",
			title: "タイトル",
			description: "説明",
			update: "説明とタイトルを更新する",
			update_error: "アップデート中に問題が発生しました",
			updated: "更新処理が完了しました",
			updating: "お待ちください",
		}
	}

})

// Injection
const apiClient: AxiosInstance | undefined = inject("apiClient");

// Define router
const route = useRoute();

// Define refs
const updateState = ref("normal");

// Define stores
const objectStore = useObjectStore();

// Define data
const fieldValidation: Record<string, boolean> = {
	descriptionModel: false,
	titleModel: false,
};

// Define onMount
onMounted(async () => {
	// Clear the source
	objectStore.$reset();

	// Get the object id
	const id: string | string[] | undefined = route.params.id;
	const destination: unknown = route.meta.destination;
	if (typeof(id) !== 'string' || isNaN(parseInt(id))) {
		// TODO - ADD ERROR HANDLING -> 400 error page
		return;
	}
	if (parseInt(id) !== parseFloat(id)) {
		// TODO - ADD ERROR HANDLING -> 400 error page
		// id is not an int
		return;
	}
	if (typeof(destination) !== 'string') {
		// TODO - ADD ERROR HANDLING -> 400 error page
		return;
	}

	await apiClient?.get(
		`/api/v1/${destination}/${id}/`
	).then(response => {
		// Specify the destination
		response.data.destination = destination;

		// Patch the data from API
		objectStore.$patch(response.data);
	}).catch((error) => {
		// TODO - Handle errors -> match the error
	});

});

// Define computed
const isUpdateButtonDisabled = computed(() => {
	return updateState.value !== "normal";
});

const renderUpdateButton = computed(() => {
	switch (updateState.value) {
		case "error":
			return t("update_error");
		case "updated":
			return t("updated");
		case "updating":
			return t("updating");
		default:
			return t("update");
	}
});

// Define functions
function updateData() {
	// Notify the user of the state change
	updateState.value = "updating"

	const CSRF_TOKEN : RegExpMatchArray | null = document.cookie.match(new RegExp(`csrftoken=([^;]+)`));
	// const csrfToken = document.head.querySelector('meta[name="csrf-token"]')?.content;
	 // || document.cookie.match(/csrftoken=([^;]+)/)?.[1];
	// console.log("csrfToken", csrfToken);
	const token = CSRF_TOKEN === null ? "" : CSRF_TOKEN[0].replace("csrftoken=", "");

	fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/`,
		{
			method: "PATCH",
			body: JSON.stringify({
				title: objectStore.title,
				description: objectStore.description,
			}),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": token,
			}
		}
	).then(() => {
		updateState.value = "updated";

		setTimeout(() => {
			updateState.value = "normal";
		}, 2000);
	}).catch((error) => {
		// TODO - handle errors property
		updateState.value = "error";

		setTimeout(() => {
			updateState.value = "normal";
		})
	});
}
</script>

<template>
	<WlkCard class="general-details">
		<WlkCardHeader>
			<h1 id="main-title">{{t(`${objectStore.destination}_details`)}}</h1>
			<p class="sub-text">{{t(`${objectStore.destination}_sub_text`)}}</p>
		</WlkCardHeader>
		<WlkTextInput
			v-model="objectStore.title"
			:label="t('title')"
			:validationRules="[required(), maxLength(255), minLength(5)]"
			:placeholderText="t(`${objectStore.destination}_title_placeholder`)"
			@isValid="(value) => (fieldValidation['titleModel'] = value)"
		/>
		<WlkTextArea
			v-model="objectStore.description"
			:label="t('description')"
			:placeholderText="t(`${objectStore.destination}_description_placeholder`)"
		/>

		<WlkButton
			class="primary"
			:isDisabled="isUpdateButtonDisabled"
			v-on:click="updateData"
		>
			{{renderUpdateButton}}
		</WlkButton>
	</WlkCard>

</template>

<style scoped>
.general-details {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem 1rem;
	}

	@media (--large-screen) {
		padding: 0.5rem 1rem;
	}
}
</style>
