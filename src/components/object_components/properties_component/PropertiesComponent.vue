<script setup lang="ts">
import {
	minValue,
	maxValue,
	WlkCard,
	WlkDatetime,
	WlkNumberInput, type OnChangeInterface,
} from 'whelk-ui'
import {useObjectStore} from "@/stores/object/object.ts";
import ObjectStatus from "@/components/object_components/object_status/ObjectStatus.vue";
import ObjectPriority from "@/components/object_components/object_priority/ObjectPriority.vue";
import {useI18n} from "petite-vue-i18n";
import {ref, nextTick, watch} from "vue";
import router from "@/router/router.ts";
import {useErrorStore} from "@/stores/error/error.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			date_invalid: "Date is not valid",
			date_updated: "Date updated",
			date_updating: "Updating date",
			end_date: "End Date",
			error_forbidden: "You do not have access to the object",
			error_not_found: "Could not find the object",
			error_server_error: "Server returned an error: ",
			properties: "Properties",
			start_date: "Start Date",
			story_point_invalid: "Invalid story points",
			story_point_updated: "Story points updated",
			story_point_updating: "Updating story points",
			story_point: "Story Points",
		},
		ja: {
			date_invalid: "日付が有効ではありません",
			date_updated: "更新日",
			date_updating: "現在、日付を更新中です。",
			end_date: "終了日",
			error_forbidden: "そのオブジェクトにアクセスする権限がありません。",
			error_not_found: "オブジェクトが見つかりませんでした。",
			error_server_error: "サーバーがエラーを返しました: ",
			properties: "プロパティ",
			start_date: "開始日",
			story_point_invalid: "無効なストーリーポイント",
			story_point_updated: "ストーリーポイントが更新されました",
			story_point_updating: "ストーリーポイントの更新",
			story_point: "ストーリーポイント",
		},
	}

})

// Define Stores
const errorStore = useErrorStore();
const objectStore = useObjectStore();

// Define refs
const dateStatus = ref<string>("");
const storyPointsStatus = ref<string>("");
const storyPointsTimeout = ref<null | ReturnType<typeof setTimeout>>(null);

// Define watches
watch(
	() => objectStore.end_date,
	async (newValue: null | string, oldValue: null | string) => {
		// If there is already a change happening - do nothing
		if (dateStatus.value !== "") {
			return;
		}

		// If nothing changes don't do anything
		if (newValue === oldValue) {
			return;
		}

		// Check to make sure the new_value is a valid date
		const date = new Date(newValue ?? 0);
		if (isNaN(date.getTime())) {
			// Not a valid date
			return;
		}

		// Notify the user of the change
		dateStatus.value = t("date_updating");

		// If start date is null set as end date
		if (objectStore.start_date === null || objectStore.start_date === "") {
			objectStore.start_date = newValue;
		}

		// If end date <  start date -> start_date = end_date
		const start_date = new Date(objectStore.start_date ?? 0);
		const end_date = new Date(newValue ?? 0);
		if (end_date < start_date) {
			objectStore.start_date = objectStore.end_date;
		}

		// Update the dates
		await datesUpdated();
	},
)

watch(
	() => objectStore.start_date,
	async (newValue: string | null, oldValue: string | null) => {
		// If there is already a change happening - do nothing
		if (dateStatus.value !== "") {
			return;
		}

		// If nothing changes don't do anything
		if (newValue === oldValue) {
			return;
		}

		// Check to make sure the new_value is a valid date
		const date = new Date(newValue ?? 0);
		if (isNaN(date.getTime())) {
			// Not a valid date
			return;
		}

		// Notify the user of the change
		dateStatus.value = t("date_updating");

		// If end date is null set as start date
		if (objectStore.end_date === null || objectStore.end_date === "") {
			objectStore.end_date = objectStore.start_date;
		}

		// If start date > end_date -> end_date = start_date
		const start_date = new Date(objectStore.start_date ?? 0);
		const end_date = new Date(objectStore.end_date ?? 0);
		if (start_date > end_date) {
			objectStore.end_date = objectStore.start_date;
		}

		// Update the dates
		await datesUpdated();
	},
)

// Define functions
async function datesUpdated() {
	const body = {
		end_date: objectStore.end_date,
		start_date: objectStore.start_date,
	}

	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/`,
			{
				method: "PATCH",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
				body: JSON.stringify(body),
			}
		);

		dateStatus.value = t("date_updated");
		handleResponseStatus(response);

		setTimeout(() => {
			dateStatus.value = "";
		}, 2000);
	} catch (error) {
		// Assuming a 500 error
		errorStore.setError(error);
		return router.push({name: "server-error"});
	}
}

function handleResponseStatus(response: Response) {
	switch (response.status) {
		case 200:
			// Everything is fine
			break;
		case 403:
			// User does not have access to the object
			errorStore.message = t("error_forbidden");
			break;
		case 404:
			// Object does not exist
			errorStore.message = t("error_not_found");
			break;
		default:
			// Assuming a 500 error
			errorStore.message = t("error_server_error");
			errorStore.showErrorModal = true;
	}
}

function storyPointsChanged(data: OnChangeInterface) {
	// Stop the timeout
	if (storyPointsTimeout.value !== null) {
		clearTimeout(storyPointsTimeout.value);
	}

	// If invalid - escape
	if (!data.isValid) {
		// Notify the user
		storyPointsStatus.value = t("story_point_invalid");

		// null the timeout
		storyPointsTimeout.value = null;

		return;
	}

	// Notify the user of the change
	storyPointsStatus.value = t("story_point_updating");

	// Set timeout - update when finished
	setTimeout(async () => {
		await storyPointsUpdate();
	}, 500);
}

async function storyPointsUpdate() {
	const body = {
		story_point: objectStore.story_point,
	}

	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/`,
			{
				method: "PATCH",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
				body: JSON.stringify(body),
			}
		);

		// Update status and check response
		storyPointsStatus.value = t("story_point_updated");
		handleResponseStatus(response);

		setTimeout(() => {
			storyPointsStatus.value = "";
		}, 2000);
	} catch (error) {
		// Assuming a 500 error
		errorStore.setError(error);
		errorStore.showErrorModal = true;
	}
}
</script>

<template>
	<WlkCard class="properties-component">
		<h3>{{ t("properties") }}</h3>

		<ObjectPriority/>
		<ObjectStatus/>

		<WlkNumberInput
			class="story-points compact"
			v-model="objectStore.story_point"
			:label="t('story_point')"
			:status="storyPointsStatus"
			:validationRules="[minValue(0), maxValue(5)]"
			v-on:change="storyPointsChanged"
		/>

		<WlkDatetime
			class="start-date compact"
			v-model="objectStore.start_date"
			:label="t('start_date')"
			:status="dateStatus"
			:disabled="dateStatus === t('date_updating')"
		/>
		<WlkDatetime
			class="end-date compact"
			v-model="objectStore.end_date"
			:label="t('end_date')"
			:status="dateStatus"
			:disabled="dateStatus === t('date_updating')"
		/>
	</WlkCard>
</template>

<style scoped>
.properties-component {
	display: grid;
	grid-template-columns: minmax(0, 1fr);
	grid-column-gap: 0.5rem;
	padding: 0 0.5rem;
	margin-bottom: 0.5rem;

	@media (--small-screen) {
		grid-template-columns: repeat(6, minmax(0, 1fr));
		grid-template-rows: 2.5rem 1fr 1fr;
	}

	@media (--medium-screen) {
		padding: 0.5rem;
	}

	@media (--large-screen) {
		grid-template-columns: minmax(0, 1fr);
		grid-template-rows: 2.5rem repeat(5, minmax(0, 1fr));
	}

	> h3 {
		margin: 0 0 1.5rem 0;

		@media (--small-screen) {
			grid-column-start: 1;
			grid-column-end: 7;
			grid-row-start: 1;
			grid-row-end: 2;
		}

		@media (--large-screen) {
			grid-column-start: 1;
			grid-column-end: 2;
		}
	}

	> .status {
		@media (--small-screen) {
			grid-column-start: 1;
			grid-column-end: 3;
			grid-row-start: 2;
			grid-row-end: 3;
		}
		@media (--large-screen) {
			grid-column-start: 1;
			grid-column-end: 2;
			grid-row-start: 2;
			grid-row-end: 3;
		}
	}

	> .priority {
		@media (--small-screen) {
			grid-column-start: 3;
			grid-column-end: 5;
			grid-row-start: 2;
			grid-row-end: 3;
		}

		@media (--large-screen) {
			grid-column-start: 1;
			grid-column-end: 2;
			grid-row-start: 3;
			grid-row-end: 4;
		}
	}

	> .story-points {
		@media (--small-screen) {
			grid-column-start: 5;
			grid-column-end: 7;
			grid-row-start: 2;
			grid-row-end: 3;
			grid-row-start: 2;
			grid-row-end: 3;
		}

		@media (--large-screen) {
			grid-column-start: 1;
			grid-column-end: 2;
			grid-row-start: 4;
			grid-row-end: 5;
		}
	}

	> .start-date {
		@media (--small-screen) {
			grid-column-start: 1;
			grid-column-end: 4;
			grid-row-start: 3;
			grid-row-end: 4;
		}
		@media (--large-screen) {
			grid-column-start: 1;
			grid-column-end: 2;
			grid-row-start: 5;
			grid-row-end: 6;
		}
	}

	> .end-date {
		@media (--small-screen) {
			grid-column-start: 4;
			grid-column-end: 7;
			grid-row-start: 3;
			grid-row-end: 4;
		}

		@media (--large-screen) {
			grid-column-start: 1;
			grid-column-end: 2;
			grid-row-start: 6;
			grid-row-end: 7;
		}
	}
}
</style>
