<script setup lang="ts">
import {
	minValue,
	maxValue,
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
import ObjectPriority from "@/components/object_components/object_priority/ObjectPriority.vue";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			end_date: "End Date",
			properties: "Properties",
			start_date: "Start Date",
			story_points: "Story Points",
		},
		ja: {
			end_date: "終了日",
			properties: "プロパティ",
			start_date: "開始日",
			story_points: "ストーリーポイント",
		},
	}

})

// Define Stores
const objectStore = useObjectStore();
</script>

<template>
	<WlkCard class="properties-component">
		<h3>{{t("properties")}}</h3>

		<ObjectPriority />
		<ObjectStatus />

		<WlkNumberInput
			class="story-points compact"
			v-model="objectStore.story_points"
			:label="t('story_points')"
			:validation="[minValue(0), maxValue(5)]"
		/>

		<WlkDatetime
			class="start-date compact"
			v-model="objectStore.start_date"
			:label="t('start_date')"
		/>
		<WlkDatetime
			class="end-date compact"
			v-model="objectStore.end_date"
			:label="t('end_date')"
		/>
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
