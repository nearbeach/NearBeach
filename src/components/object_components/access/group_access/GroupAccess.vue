<script setup lang="ts">
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {computed, ref} from "vue";
import {TrashIcon} from "@lucide/vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import {WlkRenderErrorMessage} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const objectStore = useObjectStore();
const objectMetaDataStore = useObjectMetaDataStore();
const permissionStore = usePermissionStore();

// Define refs
const errorMessage = ref<string>("");
const newGroupModel = ref<number | null | undefined>();

// Define computed
const canAddGroup = computed(() => {
	return objectMetaDataStore.availableGroupsToAdd.length > 0 && permissionStore.currentObjectPermissions.currentObject > 1;
});

const canRemoveGroup = computed(() => {
	return objectStore.group_list.length > 1 && permissionStore.currentObjectPermissions.currentObject > 1;
});

// DEFINE FUNCTIONS
async function addGroup() {
	// Null Check
	if (newGroupModel.value === null || newGroupModel.value === undefined) {
		// Nothing to do
		return;
	}

	const new_group: GroupInterface[] = objectMetaDataStore.availableGroupsToAdd.filter((row) => {
		return row.id === newGroupModel.value;
	});

	if (new_group === undefined || new_group === null || new_group.length === 0) {
		// Nothing to do
		return;
	}

	// Add group to the "group_list" optimistically
	const new_group_item : GroupInterface = new_group[0];
	objectStore.group_list.push(new_group_item);

	// Send to the backend
	const body = {
		group_list: [newGroupModel.value],
	}

	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/groups/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body)
		},
	)

	// Clear model data
	newGroupModel.value = null;

	switch (response.status) {
		case 201: {
			// Get data
			const data = await response.json();

			// Update store with correct information
			objectStore.potential_user_list = data.potential_user_list;
			objectStore.user_list = data.user_list;
			break;
		}
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			objectStore.removeGroup(new_group_item.id);
			break;
		default:
			errorMessage.value = response.statusText;
			objectStore.removeGroup(new_group_item.id);
			break;
	}
}

async function removeGroup(group_id: number) {
	// Backup
	const backup = objectStore.group_list;

	// Remove group optimistically
	objectStore.removeGroup(group_id);

	// Tell backend to remove data
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/groups/${group_id}/`,
		{
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	);

	switch (response.status) {
		case 200: {
			// Update store with correct information
			const data = await response.json();
			objectStore.potential_user_list = data.potential_user_list;
			objectStore.user_list = data.user_list;
			break;
		}
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			objectStore.group_list = backup;
			break;
		default:
			errorMessage.value = response.statusText;
			objectStore.group_list = backup;
			break;
	}
}
</script>

<template>
	<div class="group-access">
		<h3>Group Access</h3>
		<div
			v-if="objectStore.group_list.length > 0"
			class="group-access-list"
		>
			<div
				v-for="group in objectStore.group_list"
				:key="group.id"
				class="group-access-item"
			>
				<p>{{ group.name }}</p>
				<TrashIcon
					v-if="canRemoveGroup"
					v-on:click="removeGroup(group.id)"
					type="button"
					aria-label="Remove group"
				/>
			</div>
		</div>

		<WlkRenderErrorMessage v-if="errorMessage !== ''">{{ errorMessage }}</WlkRenderErrorMessage>

		<AddObject
			v-if="canAddGroup"
			label="Group"
			optionsLabel="name"
			optionsValue="id"
			:options="objectMetaDataStore.availableGroupsToAdd"
			v-model="newGroupModel"
			@change="addGroup"
		/>
		<div class="space"
		     v-if="objectMetaDataStore.availableGroupsToAdd.length === 0"
		></div>
	</div>
</template>

<style scoped>
.group-access {

	> .group-access-list {
		> .group-access-item {
			padding: 0.5rem 0;
			display: grid;
			grid-template-columns: [name] minmax(0, 1fr) [icon] 20px;

			> p {
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

			&:hover {
				background-color: var(--secondary-hover);
			}
		}
	}

	> .add-object, .space {
		margin: 1rem 0;
	}
}

</style>