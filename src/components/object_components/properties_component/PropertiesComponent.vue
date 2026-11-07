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
import {ref, watch} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";

// Define i18n
const {t} = useI18n()

// Define Stores
const objectStore = useObjectStore();

// Define refs
const dateStatus = ref<string>("");
const dateStatusClass = ref<string>("");
const storyPointsStatus = ref<string>("");
const storyPointsStatusClass = ref<string>("");
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
		dateStatus.value = t("properties_component.date_updating");

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
		dateStatus.value = t("properties_component.date_updating");

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

	const response = await safeFetch(
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

	switch (response.status) {
		case 200:
			dateStatus.value = t("properties_component.date_updated");
			dateStatusClass.value = "success";

			setTimeout(() => {
				dateStatus.value = "";
			}, 2000);
			break;
		case 403:
			dateStatus.value = t("general_detail_component.error_forbidden");
			dateStatusClass.value = "error";
			break;
		default:
			dateStatus.value = response.statusText;
			dateStatusClass.value = "error";
			break;
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
		storyPointsStatus.value = t("properties_component.story_point_invalid");

		// null the timeout
		storyPointsTimeout.value = null;

		return;
	}

	// Notify the user of the change
	storyPointsStatus.value = t("properties_component.story_point_updating");

	// Set timeout - update when finished
	storyPointsTimeout.value = setTimeout(async () => {
		await storyPointsUpdate();
	}, 500);
}

async function storyPointsUpdate() {
	const body = {
		story_point: objectStore.story_point,
	}

	const response = await safeFetch(
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

	switch (response.status) {
		case 200:
			// Update status and check response
			storyPointsStatus.value = t("properties_component.story_point_updated");
			storyPointsStatusClass.value = "success";

			setTimeout(() => {
				storyPointsStatus.value = "";
			}, 2000);
			break;
		case 403:
			storyPointsStatus.value = t("general_detail_component.error_forbidden");
			storyPointsStatusClass.value = "error";
			break;
		default:
			storyPointsStatus.value = response.statusText;
			storyPointsStatusClass.value = "error";
			break;
	}

}
</script>

<template>
	<WlkCard class="properties-component">
		<h3>{{ t("properties_component.properties") }}</h3>

		<ObjectPriority/>
		<ObjectStatus/>

		<WlkNumberInput
			class="story-points compact"
			v-model="objectStore.story_point"
			:label="t('properties_component.story_point')"
			:status="storyPointsStatus"
			:statusClass="storyPointsStatusClass"
			:validationRules="[minValue(0), maxValue(5)]"
			v-on:change="storyPointsChanged"
		/>

		<WlkDatetime
			class="start-date compact"
			v-model="objectStore.start_date"
			:label="t('properties_component.start_date')"
			:status="dateStatus"
			:statusClass="dateStatusClass"
			:disabled="dateStatus === t('properties_component.date_updating')"
		/>
		<WlkDatetime
			class="end-date compact"
			v-model="objectStore.end_date"
			:label="t('properties_component.end_date')"
			:status="dateStatus"
			:statusClass="dateStatusClass"
			:disabled="dateStatus === t('properties_component.date_updating')"
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

	> .object-priority {
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
