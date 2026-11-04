<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref, watch} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18n
const {t} = useI18n();

// Define ref
const priorityModel = ref<string>("0");
const state = ref<string>("");
const stateClass = ref<string>("");

// Define constants
const priorityList = [
	{value: 0, label: t("object_priority.highest")},
	{value: 1, label: t("object_priority.high")},
	{value: 2, label: t("object_priority.normal")},
	{value: 3, label: t("object_priority.low")},
	{value: 4, label: t("object_priority.lowest")},
]

// Define store
const objectStore = useObjectStore();

// Define subscriptions
objectStore.$subscribe((mutation, state) => {
	if (state?.priority?.value === undefined || state?.priority?.value.toString() === priorityModel.value.toString()) {
		// nothing needs to be done;
		return;
	}

	// update the model
	priorityModel.value = state.priority.value.toString();
});

// Define watchers
watch(priorityModel, async (new_value) => {
	// If new value the same in the state -> do nothing
	if (new_value === objectStore.priority.value.toString()) {
		return;
	}

	// Notify the user we are updating the status
	state.value = t("object_priority.priority_updating");
	stateClass.value = "info";

	// Fetch the status
	const priority = priorityList[parseInt(new_value)];
	if (priority === undefined) {
		// We have an issue
		state.value = "Error Updating";
		stateClass.value = "error";
		return;
	}

	objectStore.$patch({
		priority,
	});

	// Save data
	const response = await fetch(
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
	);

	switch (response.status) {
		case 200:
			state.value = t("object_priority.priority_success");
			stateClass.value = "success";

			setTimeout(() => {
				state.value = "";
			}, 5000);
			break;
		case 403:
			state.value = t("general_detail_component.error_forbidden");
			stateClass.value = "error";
			break;
		default:
			state.value = response.statusText;
			stateClass.value = "error";
			break;
	}
});
</script>

<template>
	<div class="object-priority">
		<WlkSelect
			class="status compact"
			:label="t('object_priority.label')"
			:options="priorityList"
			:status="state"
			:statusClass="stateClass"
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