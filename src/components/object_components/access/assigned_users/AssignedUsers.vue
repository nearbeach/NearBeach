<script setup lang="ts">
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {computed, ref, watch} from "vue";
import {TrashIcon} from "@lucide/vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {safeFetch} from "@/composables/safeFetch.ts";
import type {UserInterface} from "@/utils/interfaces/stores/UserInterface.ts";
import type {GroupAndUserInterface} from "@/utils/interfaces/GroupAndUsersInterface.ts";
import ProfilePicture from "@/components/prefab/profile_picture/ProfilePicture.vue";
import {WlkRenderErrorMessage} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n();

// Define ref
const errorMessage = ref<string>("");
const newAssignedUserModel = ref<number | null>(null);

// Define stores
const objectStore = useObjectStore();
const permissionStore = usePermissionStore();

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

// Define computed
const canAddUser = computed(() => {
	return objectStore.availableUsersToAdd.length > 0 && permissionStore.currentObjectPermissions.currentObject > 1;
});

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
	const new_user_item: UserInterface = new_user[0] as UserInterface;
	objectStore.user_list.push(new_user_item);

	// Send to the backend
	const body = {
		user_list: [newAssignedUserModel.value],
	}

	const response = await safeFetch(
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

	switch (response.status) {
		case 201:
			break;
		case 403:
			objectStore.removeUser(new_user_item.id);
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			objectStore.removeUser(new_user_item.id);
			errorMessage.value = response.statusText;
			break;
	}
}

async function fetchPotentialUsers() {
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/groups/`,
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	);

	switch (response.status) {
		case 200:
			// Format the response
			const data: GroupAndUserInterface = await response.json();

			// Update the potential user list
			objectStore.potential_user_list = data.potential_user_list;
			break;
		case 403:
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			errorMessage.value = response.statusText;
			break;

	}

}

async function removeUser(user_id: number) {
	// Backup
	const backup = objectStore.user_list;

	// Remove user optimistically
	objectStore.removeUser(user_id);

	// Tell backend to remove data
	const response = await safeFetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/users/${user_id}/`,
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
			objectStore.user_list = backup;
			errorMessage.value = t("general_detail_component.error_forbidden");
			break;
		default:
			objectStore.user_list = backup;
			errorMessage.value = response.statusText;
			break;
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
				<ProfilePicture :url="user.profile_picture" :name="user.first_name"/>
				<p>{{ user.first_name }} {{ user.last_name }}</p>
				<TrashIcon
					v-if="permissionStore.currentObjectPermissions.currentObject > 1"
					v-on:click="removeUser(user.id)"
					type="button"
					aria-label="Remove User"
				/>
			</div>
		</div>

		<WlkRenderErrorMessage>{{ errorMessage }}</WlkRenderErrorMessage>

		<AddObject
			v-if="canAddUser"
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

			> .profile-picture {
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