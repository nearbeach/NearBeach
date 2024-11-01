<template>
	<n-config-provider :theme="useNBTheme(theme)">
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
//Components
import GroupsAndUsersModule from "../modules/sub_modules/GroupsAndUsersModule.vue";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "KanbanGroupPermissions",
	methods: {useNBTheme},
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
