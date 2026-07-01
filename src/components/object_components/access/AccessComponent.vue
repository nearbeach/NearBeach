<script setup lang="ts">
import { WlkCard } from "whelk-ui";
import GroupAccess from "@/components/object_components/access/group_access/GroupAccess.vue";
import AssignedUsers from "@/components/object_components/access/assigned_users/AssignedUsers.vue";
</script>

<template>
	<WlkCard class="access-component">
		<GroupAccess/>
		<AssignedUsers/>
	</WlkCard>
</template>

<style scoped>
.access-component {
	padding: 0 0.5rem;
	margin-bottom: 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}
}

</style>