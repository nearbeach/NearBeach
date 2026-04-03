<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref, watch} from "vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			highest: "Highest",
			high: "High",
			normal: "Normal",
			label: "Priority",
			low: "Low",
			lowest: "Lowest",
		},
		ja: {
			highest: "最高",
			high: "高い",
			normal: "普通",
			label: "優先度",
			low: "低い",
			lowest: "最低",
		},
	}
});

// Define ref
const priorityModel = ref<string>("0");

// Define constants
const priorityList = [
	{value: 0, label: t("highest")},
	{value: 1, label: t("high")},
	{value: 2, label: t("normal")},
	{value: 3, label: t("low")},
	{value: 4, label: t("lowest")},
]

// Define store
const objectMetaDataStore = useObjectMetaDataStore();
const objectStore = useObjectStore();

// Define subscribes
objectStore.$subscribe((mutation, state) => {
	if (state?.priority?.value === undefined || state?.priority?.value.toString() === priorityModel.value.toString()) {
		// nothing needs to be done;
		return;
	}

	// update the model
	priorityModel.value = state.priority.value.toString();
});

// Define watchers
watch(priorityModel, (new_value) => {
	if (new_value === "0") {
		// Nothing to do
		return;
	}

	// Fetch the status
	const priority = priorityList[parseInt(new_value)];
	if (priority === undefined) {
		// We have an issue
		// TODO - Do propper error handling
		console.error(`Status was not found in state management: ${new_value}`)
		return;
	}

	objectStore.$patch({
		priority: priority,
	});
});
</script>

<template>
	<WlkSelect
		class="status compact"
		:label="t('label')"
		:options="priorityList"
		:validationRules="[required()]"
		v-model="priorityModel"
	/>
</template>

<style scoped>

</style>