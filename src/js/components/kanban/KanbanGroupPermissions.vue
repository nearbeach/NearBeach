<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card kanban-group-permissions">
			<div class="card-body">
				<!-- Group Permissions -->
				<groups-and-users-module
					v-bind:is-read-only="isReadOnly"
				></groups-and-users-module>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import getThemeMixins from "../../mixins/getThemeMixin"
import GroupsAndUsersModule from "../modules/sub_modules/GroupsAndUsersModule.vue";

export default {
	name: "KanbanGroupPermissions",
	mixins: [getThemeMixins],
	props: {
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		theme: {
			type: String,
			default: "",
		},
	},
	components: {
		GroupsAndUsersModule,
	},
};
</script>
