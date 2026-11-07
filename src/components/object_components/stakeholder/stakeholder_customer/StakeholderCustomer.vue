<script setup lang="ts">
import {useObjectStore} from "@/stores/object/object.ts";
import {TrashIcon} from "@lucide/vue";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {ref} from "vue";
import {WlkRenderErrorMessage} from "whelk-ui";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import {useI18n} from "petite-vue-i18n";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const objectStore = useObjectStore();
const objectMetaDataStore = useObjectMetaDataStore();
const permissionStore = usePermissionStore();

// Define ref
const customerModel = ref<number>(0);
const errorMessage = ref<string>("");

// Define functions
async function addCustomer() {
	if (customerModel.value === 0 || customerModel.value === undefined || customerModel.value === null) {
		// Nothing to do
		return;
	}

	const body = {
		id: customerModel.value,
	}

	const response = await safeFetch(
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

	switch (response.status) {
		case 201:
			// Get data
			objectStore.customers = await response.json();
			break;
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			errorMessage.value = response.statusText;
			break;
	}
}

async function removeCustomer(customer_id: number) {
	// Backup
	const backup = objectStore.customers;

	// Optimistically remove customer id
	objectStore.removeCustomer(customer_id);

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/customer/${customer_id}/`,
		{
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	)

	switch (response.status) {
		case 204:
			break;
		case 403:
			objectStore.customers = backup;
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			objectStore.customers = backup;
			errorMessage.value = response.statusText;
			break;
	}
}
</script>

<template>
	<div class="stakeholder-customer">
		<WlkRenderErrorMessage>{{ errorMessage }}</WlkRenderErrorMessage>
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
				v-if="permissionStore.currentObjectPermissions.currentObject > 1"
				v-on:click="removeCustomer(customer.id)"
				type="button"
				aria-label="Remove User"
			/>
		</div>
		<AddObject
			v-if="permissionStore.currentObjectPermissions.currentObject > 1"
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