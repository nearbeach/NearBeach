<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {ref, watch} from "vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {useI18n} from "petite-vue-i18n";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			label: "Status",
			status_success: "Successfully updated status",
			status_updating: "Updating Status",
		},
		ja: {
			label: "状態",
			status_success: "ステータスの更新に成功しました",
			status_updating: "ステータスを更新中",
		},
	}
})

// Define ref
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
watch(statusModel, (new_value) => {
	if (new_value === "0") {
		// Nothing to do
		return;
	}
	console.log("NEW VALUE: ", new_value);

	// If new value is the same as the state - do nothing
	if (new_value === objectStore.status.id.toString()) {
		return;
	}

	// Fetch the status
	const status = objectMetaDataStore.fetchStatus(parseInt(new_value));
	if (status.length === 0) {
		// We have an issue
		// TODO - Do propper error handling
		console.error(`Status was not found in state management: ${new_value}`)
		return;
	}

	objectStore.$patch({
		status: status[0],
	});

	statusMessage.value = t("status_updating");

	// Save data
	fetch(
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
	).then(() => {
		statusMessage.value = t("status_success");

		setTimeout(() => {
			statusMessage.value = "";
		}, 5000);
	}).catch((error) => {
		// TODO - handle errors properly
		statusMessage.value = "Error Updating";
		console.error(error);
	});
})
</script>

<template>
	<WlkSelect
		class="status compact"
		optionsLabel="status"
		optionsValue="id"
		:label="t('label')"
		:options="objectMetaDataStore.status"
		:status="statusMessage"
		:validationRules="[required()]"
		v-model="statusModel"
	/>
</template>

<style scoped>

</style>