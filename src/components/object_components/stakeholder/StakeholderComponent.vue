<script setup lang="ts">
import StakeholderOrganisation
	from "@/components/object_components/stakeholder/stakeholder_organisation/StakeholderOrganisation.vue";
import StakeholderCustomer
	from "@/components/object_components/stakeholder/stakeholder_customer/StakeholderCustomer.vue";
import {WlkCard, WlkCardHeader} from "whelk-ui";
import {useObjectStore} from "@/stores/object/object.ts";
import {onMounted, watch} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";

// Define stores
const objectStore = useObjectStore();
const objectMetaDataStore = useObjectMetaDataStore();

// Watch a specific state property
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await loadData();
		}
	}
)

// Define onMount
onMounted(async () => {
	// Only load data if the object has loaded in
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define functions
async function loadData() {
	// TODO - look at state - and showing users what state the data is currently in, i.e. "Loading"
	// State we are loading
	// isLoaded.value = false;

	// Fetch the required data
	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/organisation/`,
			{
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
			},
		);

		// Fetch data
		const data = await response.json();

		// Set data
		objectStore.customers = data.customers;
		objectStore.organisation = data.organisation;

		// Set data meta
		objectMetaDataStore.potential_customers = data.potential_customers ?? [];
		objectMetaDataStore.potential_organisations = data.potential_organisations ?? [];
	} catch(error) {
		// TODO - handle error
		console.error(error);
	}
}

</script>

<template>
	<WlkCard class="stakeholder-component">
		<WlkCardHeader>
			<h3>Stakeholders</h3>
		</WlkCardHeader>

		<StakeholderOrganisation/>
		<StakeholderCustomer/>
	</WlkCard>
</template>

<style scoped>
.stakeholder-component {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}
}
</style>