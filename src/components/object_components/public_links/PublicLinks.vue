<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import type {PublicLinkInterface} from "@/utils/interfaces/PublicLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import {WlkButton, WlkRenderErrorMessage} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import PublicLinkRow from "@/components/object_components/public_links/public_link_row/PublicLinkRow.vue";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n()

// Define stores
const objectStore = useObjectStore();
const permissionStore = usePermissionStore();

// Define refs
const errorMessage = ref<string>("");
const errorMessageCreate = ref<string>("");
const publicLinks = ref<PublicLinkInterface[]>([]);

// Define watch
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await loadData();
		}
	}
);

// Define onMounted
onMounted(async () => {
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define functions
async function createPublicLink() {
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/public_link/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	);

	switch (response.status) {
		case 201: {
			const data = await response.json();
			publicLinks.value.push(data);
			break;
		}
		case 403:
			errorMessageCreate.value = t("general_detail_component.error_forbidden");
			break;
		default:
			errorMessageCreate.value = response.statusText;
			break;
	}
}

async function deleteLink(data: { id: string }) {
	// Backup
	const backup_public_links = publicLinks.value;

	// Remove the link from the publicLinks list
	publicLinks.value = publicLinks.value.filter((link) => {
		return link.id !== data.id;
	});

	// Tell the backend to delete the link
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/public_link/${data.id}/`,
		{
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	);

	switch (response.status) {
		case 204:
			break;
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			publicLinks.value = backup_public_links;
			break;
		default:
			errorMessage.value = response.statusText;
			publicLinks.value = backup_public_links;
			break;
	}
}

async function loadData() {
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/public_link/`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
			}
		}
	)

	switch (response.status) {
		case 200: {
			const data = await response.json();
			publicLinks.value = data;
			break;
		}
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			errorMessage.value = response.statusText;
			break;
	}
}

async function updateActive(data: { id: string, index: number }) {
	// Check user access first
	if (permissionStore.currentObjectPermissions.currentObject <= 1) {
		// Do nothing silently
		return;
	}

	// Get copy of data
	const public_link_row = publicLinks.value[data.index];

	// Checks and balances
	if (public_link_row === undefined || public_link_row === null) {
		// Notify the user we could not find the public link
		errorMessage.value = t("public_links.error_public_link_not_found");
		return;
	}

	// Mutate the data
	public_link_row.is_active = !public_link_row.is_active;

	// Update the data
	publicLinks.value[data.index] = public_link_row;

	// Update the backend
	const body = {
		is_active: public_link_row.is_active,
	}

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/public_link/${data.id}/`,
		{
			method: "PATCH",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		}
	)

	switch (response.status) {
		case 200:
			break;
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			public_link_row.is_active = !public_link_row.is_active;
			publicLinks.value[data.index] = public_link_row;
			break;
		default:
			errorMessage.value = response.statusText;
			public_link_row.is_active = !public_link_row.is_active;
			publicLinks.value[data.index] = public_link_row;
	}
}
</script>

<template>
	<div class="public-links">
		<h3>{{ t("public_links.public_link") }}</h3>
		<p class="sub-text">{{ t("public_links.description") }}</p>

		<div class="empty-public-links-list"
		     v-if="publicLinks.length === 0"
		>
			{{ t("public_links.empty_public_links") }}
		</div>

		<WlkRenderErrorMessage>{{ errorMessage }}</WlkRenderErrorMessage>

		<table v-if="publicLinks.length > 0">
			<thead>
			<tr>
				<td style="width:calc(100% - 110px);">{{ t("public_links.public_link") }}</td>
				<td style="width:90px;">{{ t("public_links.is_active") }}</td>
				<td style="width:20px;"
					v-if="permissionStore.currentObjectPermissions.currentObject > 1"
				></td>
			</tr>
			</thead>
			<tbody>
			<tr v-for="(link, index) in publicLinks"
			    :key="link.id"
			>
				<PublicLinkRow :id="link.id"
				               :is-active="link.is_active"
				               :index="index"
				               v-on:delete-link="deleteLink"
				               v-on:update-active="updateActive"
				/>
			</tr>
			</tbody>
		</table>

		<div class="public-link-buttons"
			 v-if="permissionStore.currentObjectPermissions.currentObject > 1"
		>
			<WlkRenderErrorMessage>{{ errorMessageCreate }}</WlkRenderErrorMessage>
			<WlkButton class="compact primary"
			           @click="createPublicLink"
			>
				{{ t("public_links.create_public_link") }}
			</WlkButton>
		</div>
	</div>
</template>

<style scoped>
.public-links {
	.empty-public-links-list {
		margin-top: 2rem;
		height: 7rem;
		display: flex;
		justify-content: center;
		align-items: center;
		font-size: 1.25rem;
		font-weight: 100;
		font-family: "Roboto", sans-serif;
		border: dashed;
		border-radius: var(--border-radius);
		border-width: var(--border-width);
	}

	> table {
		table-layout: fixed;
		width: 100%;
		display: table;

		> thead > tr {
			font-weight: bold;
			font-size: 1.25rem;
			border: none;

			> td {
				border: none;
			}
		}

		> tbody > tr {
			font-weight: lighter;
			font-size: 1rem;
			border: none;

			> td {
				border: none;
			}
		}

		> tbody > tr:nth-child(odd) {
			background-color: var(--bg-dark);
		}
	}

	> .public-link-buttons {
		margin-top: 0.75rem;
	}
}

</style>