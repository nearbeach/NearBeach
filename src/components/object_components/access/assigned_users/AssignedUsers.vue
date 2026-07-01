<script setup lang="ts">
import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {ObjectTitleCaseEnums} from "@/utils/enums/ObjectTitleCaseEnums.ts";
import {type PropType, ref} from "vue";
import {TrashIcon} from "@lucide/vue";
import {useObjectStore} from "@/stores/object/object.ts";

// Define ref
const newAssignedUserModel = ref("");

// Define stores
const objectStore = useObjectStore();

// DEFINE FUNCTIONS
function addUser(user_id: number) {
	// ADD CODE
}
function removeUser(user_id: number) {
	// ADD CODE
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
				<p>{{ user.name }}</p>
				<TrashIcon
					v-on:click="removeUser(user.id)"
					type="button"
					aria-label="Remove User"
				/>
			</div>
		</div>

		<AddObject
			label="Users"
			optionsLabel="name"
			optionsValue="id"
			:options="objectStore.potential_user_list"
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
			grid-template-columns: [profile] 20px [name] minmax(0, 1fr) [icon] 20px;

			> img {
				width: 20px;
				height: 20px;
				object-fit: cover;
				border-radius: 50%;
				transform: translateY(5px);
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