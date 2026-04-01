<script setup lang="ts">
import {computed, ref} from "vue";
import {
	WlkCard,
	WlkDatetime,
	WlkTextInput,
	WlkNumberInput,
	WlkSelect,
	required,
	type SelectOptionInterface
} from 'whelk-ui'
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import ObjectStatus from "@/components/object_components/object_status/ObjectStatus.vue";

// Define Stores
const objectStore = useObjectStore();

const priorityModel = ref("HIGH PRIORITY")


// Define Data
// TODO - Move fieldValidation: Record<string, boolean> into Object store
// const fieldValidation: Record<string, boolean> = {
// 	// endDateModel: true,
// 	priorityModel: true,
// 	// startDateModel: true,
// 	statusModel: true,
// };
</script>

<template>
	<WlkCard class="properties-component">
		<h3>Properties</h3>

		<WlkTextInput
			class="priority compact"
			v-model="priorityModel"
			label="Priority"
			@isValid="(value) => (fieldValidation['priorityModel'] = value)"
		/>

		<ObjectStatus class="status compact" />

		<WlkNumberInput
			class="story-points compact"
			v-model="objectStore.story_points"
			label="Story Points"
			:min-value="0"
			:max-value="10"
		/>

		<!--        <WlkDatetime-->
		<!--            class="start-date compact"-->
		<!--            v-model="startDateModel"-->
		<!--            label="Start Date"-->
		<!--            @isValid="(value) => (fieldValidation['startDateModel'] = value)"-->
		<!--        />-->
		<!--        <WlkDatetime-->
		<!--            class="end-date compact"-->
		<!--            v-model="endDateModel"-->
		<!--            label="End Date"-->
		<!--            @isValid="(value) => (fieldValidation['endDateModel'] = value)"-->
		<!--        />-->
	</WlkCard>
</template>

<style scoped>
.properties-component {
	display: grid;
	grid-template-columns: minmax(0, 1fr);
	grid-column-gap: 0.5rem;
	padding: 0 0.5rem;

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
