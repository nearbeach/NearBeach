<template>
	<div class="card kanban-group-permissions">
		<div class="card-body">
			<!-- Group Permissions -->
			<groups-and-users-module
			></groups-and-users-module>
		</div>
	</div>
</template>

<script>
	import GroupsAndUsersModule from "../modules/sub_modules/GroupsAndUsersModule.vue";

	export default {
		name: "KanbanGroupPermissions",
		components: {
			GroupsAndUsersModule,
		},
	};
</script>
