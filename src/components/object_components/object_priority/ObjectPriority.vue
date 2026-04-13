<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref, watch} from "vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

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
			priority_success: "Successfully updated priority",
			priority_updating: "Updating Priority",
		},
		ja: {
			highest: "最高",
			high: "高い",
			normal: "普通",
			label: "優先度",
			low: "低い",
			lowest: "最低",
			priority_success: "優先度の更新に成功しました",
			priority_updating: "優先度を更新中",
		},
	}
});

// Define ref
const priorityModel = ref<string>("0");
const state = ref<string>("");

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

	// If new value the same in the state - do nothing
	if (new_value === objectStore.priority.value.toString()) {
		return;
	}

	state.value = t("priority_updating");

	// Fetch the status
	const priority = priorityList[parseInt(new_value)];
	if (priority === undefined) {
		// We have an issue
		// TODO - Do propper error handling
		console.error(`Status was not found in state management: ${new_value}`)
		state.value = "Error Updating";
		return;
	}

	objectStore.$patch({
		priority: priority,
	});

	// Save data
	fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/`,
		{
			method: "PATCH",
			body: JSON.stringify({
				priority: new_value,
			}),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	).then(() => {
		state.value = t("priority_success");

		setTimeout(() => {
			state.value = "";
		}, 5000);
	}).catch((error) => {
		// TODO - handle errors properly
		state.value = "Error Updating";
		console.error(error);
	});
});
</script>

<template>
	<div class="object-priority">
		<WlkSelect
			class="status compact"
			:label="t('label')"
			:options="priorityList"
			:status="state"
			:validationRules="[required()]"
			v-model="priorityModel"
		/>
	</div>
</template>

<style scoped>
.object-priority {
	> p {
		font-size: 0.75rem;
		color: hotpink;
	}
}

</style>