<script setup lang="ts">
import { ref } from "vue";
import CardComponent from "@/components/prefab/card/CardComponent.vue";
import GroupAccess from "@/components/project/project_page/access/group_access/GroupAccess.vue";
import UserAccess from "@/components/project/project_page/access/user_access/UserAccess.vue";

// DECLARE REF
const groupList = ref<{group_id: number, group_name: string}[]>([
	{group_id: 1, group_name: "Administration"},
	{group_id: 2, group_name: "QA Team"},
	{group_id: 3, group_name: "Developers"},
]);

const userList = ref<{user_id: number, user_name: string}[]>([
	{user_id: 1, user_name: "Administration"},
	{user_id: 2, user_name: "Frank Miller"},
	{user_id: 3, user_name: "Oscar Fluffy"},
	{user_id: 4, user_name: "Socks Fluffy Butt"},
]);

// DECLARE FUNCTIONS
function removeGroup(group_id: number) {
	groupList.value = groupList.value.filter((row) => {
		return row.group_id !== group_id;
	});
}

function removeUser(user_id: number) {
	userList.value = userList.value.filter((row) => {
		return row.user_id !== user_id;
	});
}
</script>

<template>
	<CardComponent class="access-component">
		<GroupAccess
			:group-list="groupList"
			v-on:remove-group="removeGroup"
		/>
		<UserAccess
			:user-list="userList"
			v-on:remove-user="removeUser"
		/>
	</CardComponent>
</template>

<style scoped>
.access-component {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}
}

</style>