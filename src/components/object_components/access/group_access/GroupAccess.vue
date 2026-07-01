<script setup lang="ts">
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {nextTick, type PropType} from "vue";
import { ref} from "vue";
import {TrashIcon} from "@lucide/vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import type {GroupInterface} from "@/utils/interfaces/stores/GroupInterface.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// DEFINE EMITS
const emit = defineEmits([
	'removeGroup',
]);

// Define stores
const objectStore = useObjectStore();
const objectMetaDataStore = useObjectMetaDataStore();

// Define refs
const newGroupModel = ref<number | null | undefined>();

// DEFINE FUNCTIONS
async function addGroup() {
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
	objectStore.group_list.push(new_group[0] as GroupInterface);

	// Wipe it clean on the next tick
	await nextTick(() => {
		newGroupModel.value = null;
	});

	// Send to the backend
	const body = {
		group_list: [newGroupModel.value],
	}

	try {
		const response = await fetch(
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

		// TODO - update the potential user list
	} catch (e) {
		// TODO - handle the errors
		console.error("ERROR: ", e);
	}
}

function removeGroup(group_id: number) {
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
					v-if="objectStore.group_list.length > 1"
					v-on:click="removeGroup(group.id)"
					type="button"
					aria-label="Remove group"
				/>
			</div>
		</div>

		<AddObject
			label="Group"
			optionsLabel="name"
			optionsValue="id"
			:options="objectMetaDataStore.availableGroupsToAdd"
			v-model="newGroupModel"
			@change="addGroup"
		/>
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

	> .add-object {
		margin: 1rem 0;
	}
}

</style>