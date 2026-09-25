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
import {computed, ref} from "vue";
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
			story_points: "Story Points",
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
			story_points: "ストーリーポイント",
		},
	}

})

// Define Stores
const errorStore = useErrorStore();
const objectStore = useObjectStore();

// Define refs
const dateTimeout = ref<null | ReturnType<typeof setTimeout>>(null);
const endDateStatus = ref<string>("");
const startDateStatus = ref<string>("");
const storyPointsStatus = ref<string>("");
const storyPointsTimeout = ref<null | ReturnType<typeof setTimeout>>(null);


// Define computed
const endDate = computed(() => {
	if (objectStore.end_date === null) {
		return "";
	}

	return objectStore.end_date;
});

const startDate = computed(() => {
	if (objectStore.start_date === null) {
		return "";
	}

	return objectStore.start_date;
});

// Define functions
async function endDateChanged(data: OnChangeInterface) {
	// Stop the timeout
	if (dateTimeout.value !== null) {
		clearTimeout(dateTimeout.value);
	}

	// If invalid - escape
	if (!data.isValid) {
		// Notify the user
		endDateStatus.value = t("date_invalid");

		// null the timeout
		dateTimeout.value = null;

		return;
	}

	// Notify the user of the change
	endDateStatus.value = t("date_updating");

	// Set timeout - update when finished
	setTimeout(async () => {
		await datesUpdated();
	}, 500);
}

async function startDateChanged(data: OnChangeInterface) {
	// Stop the timeout
	if (dateTimeout.value !== null) {
		clearTimeout(dateTimeout.value);
	}

	// If invalid - escape
	if (!data.isValid) {
		// Notify the user
		endDateStatus.value = t("date_invalid");

		// null the timeout
		dateTimeout.value = null;

		return;
	}

	// Notify the user of the change
	endDateStatus.value = t("date_updating");

	// Set timeout - update when finished
	setTimeout(async () => {
		await datesUpdated();
	}, 500);
}

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

		startDateStatus.value = t("date_updated");
		endDateStatus.value = t("date_updated");
		handleResponseStatus(response);

		setTimeout(() => {
			startDateStatus.value = "";
			endDateStatus.value = "";
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
			errorStore.setError(response);
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
		story_points: objectStore.story_points,
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
			v-model="objectStore.story_points"
			:label="t('story_points')"
			:status="storyPointsStatus"
			:validationRules="[minValue(0), maxValue(5)]"
			v-on:change="storyPointsChanged"
		/>

		<WlkDatetime
			class="start-date compact"
			v-model="startDate"
			:label="t('start_date')"
			:status="startDateStatus"
			v-on:change="startDateChanged"
		/>
		<WlkDatetime
			class="end-date compact"
			v-model="endDate"
			:label="t('end_date')"
			:status="endDateStatus"
			v-on:change="endDateChanged"
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
