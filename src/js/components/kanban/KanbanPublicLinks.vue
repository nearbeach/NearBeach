<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<list-public-links
					:is-read-only="isReadOnly"
					override-destination="kanban_board"
					:override-location-id="locationId"
				></list-public-links>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Component
import ListPublicLinks from "Modules/sub_modules/ListPublicLinks.vue"

//Composables
import {useNBTheme} from "Composables/theme/useNBTheme";

export default {
	name: "KanbanPublicLinks",
	components: {
		ListPublicLinks,
	},
	props: {
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		locationId: {
			type: Number,
			default: 0,
		},
		theme: {
			type: String,
			default: "",
		},
	},
	methods: {useNBTheme},
}
</script>