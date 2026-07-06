<script setup lang="ts">
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {nextTick, onMounted, ref, watch} from "vue";
import {TrashIcon} from "@lucide/vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {UserInterface} from "@/utils/interfaces/stores/UserInterface.ts";
import type {GroupAndUserInterface} from "@/utils/interfaces/GroupAndUsersInterface.ts";

// Define ref
const newAssignedUserModel = ref<number | null>(null);

// Define stores
const objectStore = useObjectStore();

// Watch a specific state property
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await fetchPotentialUsers();
		}
	}
)

// DEFINE FUNCTIONS
async function addUser() {
	if (newAssignedUserModel.value === null || newAssignedUserModel.value === undefined) {
		// Nothing to do
		return;
	}

	const new_user = objectStore.potential_user_list.filter((row) => {
		return row.id === newAssignedUserModel.value;
	})

	if (new_user === undefined || new_user === null || new_user.length === 0) {
		// Nothing to do
		return;
	}

	// Add group to the "group_list" optimistically
	objectStore.user_list.push(new_user[0] as UserInterface);

	// Send to the backend
	const body = {
		user_list: [newAssignedUserModel.value],
	}

	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/users/`,
			{
				method: "POST",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
				body: JSON.stringify(body)
			},
		)

		// Clear model
		newAssignedUserModel.value = null;
	} catch (e) {
		// TODO - handle the errors
		console.error("ERROR: ", e);
	}
}

async function fetchPotentialUsers() {
	try {
		const response = await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/groups/`,
			{
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
			},
		);

		// Format the response
		const data : GroupAndUserInterface = await response.json();

		// Update the potential user list
		objectStore.potential_user_list = data.potential_user_list;
	} catch (error) {
		// TODO - handle errors
		console.log("ERROR: ", error);
	}
}

async function removeUser(user_id: number) {
	// Remove user optimistically
	objectStore.removeUser(user_id);

	// Tell backend to remove data
	try {
		await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/users/${user_id}/`,
			{
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
			},
		);

		// TODO handle the response and update the potential users and user list
	} catch (error) {
		console.log("ERROR: ", error);
		// TODO - handle error
	}
}

</script>

<template>
	<div class="user-access">
		<h3>Assigned Users</h3>
		<div
			v-if="objectStore.user_list.length > 0"
			class="user-access-list"
		>
			<div
				v-for="user in objectStore.user_list"
				:key="user.id"
				class="user-access-item"
			>
				<img
					src="https://nearbeach.org/media/gkgmptvg/bee-socks.jpg?width=120"
					alt="User Profile Picture"
				/>
				<p>{{ user.first_name }} {{ user.last_name }}</p>
				<TrashIcon
					v-on:click="removeUser(user.id)"
					type="button"
					aria-label="Remove User"
				/>
			</div>
		</div>

		<AddObject
			label="Users"
			optionsLabel="full_name"
			optionsValue="id"
			:options="objectStore.availableUsersToAdd"
			v-model="newAssignedUserModel"
			@change="addUser"
		/>
	</div>
</template>

<style scoped>
.user-access {
	> .user-access-list {
		> .user-access-item {
			padding: 0.5rem 0;
			display: grid;
			grid-template-columns: [profile] 25px [name] minmax(0, 1fr) [icon] 20px;

			> img {
				width: 20px;
				height: 20px;
				object-fit: cover;
				border-radius: 50%;
				transform: translateY(2px);
				grid-area: profile;
			}


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