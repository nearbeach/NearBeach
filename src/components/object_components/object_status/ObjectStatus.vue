<script setup lang="ts">
import {required, type SelectOptionInterface, WlkSelect} from "whelk-ui";
import {computed, ref, watch} from "vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {storeToRefs} from 'pinia'

// Define ref
const statusModel = ref("0");

// Define store
const objectMetaDataStore = useObjectMetaDataStore();
const objectStore = useObjectStore();

// Define subscribes
objectStore.$subscribe((mutation, state) => {
	if (state?.status?.id === undefined || state?.status?.id === statusModel.value) {
		// nothing needs to be done;
		return;
	}

	// update the model
	statusModel.value = state.status.id;
});

// Define watchers
watch(statusModel, (new_value) => {
	if (new_value === 0) {
		// Nothing to do
		return;
	}

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
})

// Define computed
const tempStatusCodes = computed(() => {
	return objectMetaDataStore.status.map((row) => {
		const data: SelectOptionInterface = {
			value: row.id.toString() as string,
			label: row.status as string,
			disabled: false,
			optGroup: "",
		}

		return data
	});
});
</script>

<template>
	<WlkSelect
		label="Status"
		:options="tempStatusCodes"
		:validationRules="[required()]"
		v-model="statusModel"
	/>
</template>

<style scoped>

</style>