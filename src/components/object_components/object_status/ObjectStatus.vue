<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {ref, watch} from "vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {useI18n} from "petite-vue-i18n";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";

// Define i18n
const {t} = useI18n()

// Define ref
const statusClass = ref<string>("");
const statusModel = ref<string>("0");
const statusMessage = ref<string>("");

// Define store
const objectMetaDataStore = useObjectMetaDataStore();
const objectStore = useObjectStore();

// Define subscribes
objectStore.$subscribe((mutation, state) => {
	if (state?.status?.id === undefined || state?.status?.id.toString() === statusModel.value.toString()) {
		// nothing needs to be done;
		return;
	}

	// update the model
	statusModel.value = state.status.id.toString();
});

// Define watchers
watch(statusModel, async (new_value) => {
	if (new_value === "0") {
		// Nothing to do
		return;
	}

	// If the new value is the same as the state - do nothing
	if (new_value === objectStore.status.id.toString()) {
		return;
	}

	// Fetch the status
	const status = objectMetaDataStore.fetchStatus(parseInt(new_value));
	if (status.length === 0) {
		// We have an issue
		statusMessage.value = "Error Updating";
		statusClass.value = "error";
		return;
	}

	objectStore.$patch({
		status: status[0],
	});

	statusMessage.value = t("object_status.status_updating");
	statusClass.value = "info";

	// Save data
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/`,
		{
			method: "PATCH",
			body: JSON.stringify({
				status: new_value,
			}),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	)

	switch (response.status) {
		case 200:
			statusMessage.value = t("object_status.status_success");
			statusClass.value = "success";

			setTimeout(() => {
				statusMessage.value = "";
			}, 5000);
			break;
		case 403:
			statusMessage.value = t("general_detail_component.error_forbidden");
			statusClass.value = "error";
			break;
		default:
			statusMessage.value = response.statusText;
			statusClass.value = "error";
			break;
	}
})
</script>

<template>
	<WlkSelect
		class="status compact"
		optionsLabel="status"
		optionsValue="id"
		:label="t('object_status.label')"
		:options="objectMetaDataStore.status"
		:status="statusMessage"
		:validationRules="[required()]"
		v-model="statusModel"
	/>
</template>