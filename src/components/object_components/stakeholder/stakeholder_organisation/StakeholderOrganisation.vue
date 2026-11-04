<script setup lang="ts">
import {TrashIcon} from "@lucide/vue";
import {useObjectStore} from "@/stores/object/object.ts";
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {OrganisationLinkInterface} from "@/utils/interfaces/stores/OrganisationLinkInterface.ts";
import {WlkRenderErrorMessage} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n();

// Define stores
const objectStore = useObjectStore();
const objectMetaDataStore = useObjectMetaDataStore();

// Define refs
const errorMessage = ref<string>("");
const organisationModel = ref<number>(0);

// Define functions
async function addOrganisation() {
	// Make sure organisation Model is not 0 or null
	if (organisationModel.value === 0 || organisationModel.value === null || organisationModel.value === undefined) {
		// Nothing to do
		return;
	}

	// Send request to backend
	const body = {
		id: organisationModel.value,
	}

	const response = await fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/organisation/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		},
	)

	// Check response status
	switch (response.status) {
		case 201:
			// Set data in store
			const data: OrganisationLinkInterface = await response.json();

			// Object Store
			objectStore.customers = [];
			objectStore.organisation = data.organisation;

			// Object Data Meta Store
			objectMetaDataStore.potential_customers = data.potential_customers ?? [];
			break;
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			errorMessage.value = response.statusText;
			break;
	}
}

async function removeOrganisation() {
	// Backup
	const backup = objectStore.organisation;

	// Optimistically remove organisation id
	objectStore.organisation = null;

	const response = await fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/organisation/`,
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
			objectStore.organisation = backup;
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			objectStore.organisation = backup;
			errorMessage.value = response.statusText;
			break;
	}
}
</script>

<template>
	<div class="stakeholder-organisation">
		<WlkRenderErrorMessage>{{ errorMessage }}</WlkRenderErrorMessage>
		<p v-if="objectStore?.organisation !== null">Organisation</p>
		<div
			class="organisation-name"
			v-if="objectStore?.organisation !== null"
		>
			<RouterLink :to="`organisation/${objectStore?.organisation?.id}`">
				{{ objectStore?.organisation.name }}
			</RouterLink>
			<TrashIcon
				v-on:click="removeOrganisation()"
				type="button"
				aria-label="Remove User"
			/>
		</div>
		<div v-else>
			<AddObject
				label="Organisation"
				optionsLabel="name"
				optionsValue="id"
				:options="objectMetaDataStore.potential_organisations"
				v-model="organisationModel"
				@change="addOrganisation"
			/>
		</div>
	</div>
</template>

<style scoped>
.stakeholder-organisation {
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