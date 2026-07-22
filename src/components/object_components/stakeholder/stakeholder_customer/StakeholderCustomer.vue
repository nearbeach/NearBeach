<script setup lang="ts">
import {useObjectStore} from "@/stores/object/object.ts";
import {TrashIcon} from "@lucide/vue";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";

// Define stores
const objectStore = useObjectStore();
const objectMetaDataStore = useObjectMetaDataStore();

// Define ref
const customerModel = ref<number>(0);

// Define functions
async function addCustomer() {
	if (customerModel.value === 0 || customerModel.value === undefined || customerModel.value === null) {
		// Nothing to do
		return;
	}

	// Optimistically add the customer to the list
	// TODO - implement this code

	const body = {
		id: customerModel.value,
	}

	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/customer/`,
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
				body: JSON.stringify(body),
			},
		);

		// Get data
		objectStore.customers = await response.json();
	} catch (error) {
		// TODO - Add better error handline
		console.error(error);
	}
}

async function removeCustomer(customer_id: number) {
	// Optimistically remove customer id
	objectStore.removeCustomer(customer_id);

	try {
		await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/customer/${customer_id}/`,
			{
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
			},
		)
	} catch (errors) {
		// TODO - implement correct error handling
		console.error(errors);
	}
}

// TODO - Add in on mount to fetch current customers associated with this object

</script>

<template>
	<div class="stakeholder-customer">
		<p>Customers</p>
		<div
			v-for="customer in objectStore?.customers"
			class="customer-name"
			:key="customer.id"
		>
			<RouterLink :to="`customer/${customer.id}`">
				{{ customer.first_name }} {{ customer.last_name }}
			</RouterLink>
			<TrashIcon
				v-on:click="removeCustomer(customer.id)"
				type="button"
				aria-label="Remove User"
			/>
		</div>
		<AddObject
			label="Customer"
			optionsLabel="first_name"
			optionsValue="id"
			:options="objectMetaDataStore?.potential_customers"
			v-model="customerModel"
			@change="addCustomer"
		/>
	</div>
</template>

<style scoped>
.stakeholder-customer {
	> p {
		font-size: 0.75rem;
		line-height: 1rem;
	}

	> .organisation-name {
		display: grid;
		grid-template-columns: [name] minmax(0, 1fr) [icon] 20px;

		> a {
			grid-area: name;
			overflow: hidden;
			white-space: nowrap;
			text-overflow: ellipsis;
			padding: 0;
			margin: 0;
			font-size: 1rem;
		}

		> svg {
			grid-area: icon;
			width: 20px;
			height: 20px;
		}
	}
}

</style>