<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<list-public-links
					v-bind:is-read-only="isReadOnly"
					override-destination="kanban_board"
					v-bind:override-location-id="locationId"
				></list-public-links>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Component
import ListPublicLinks from "../modules/sub_modules/ListPublicLinks.vue"

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "KanbanPublicLinks",
	methods: {useNBTheme},
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
	components: {
		ListPublicLinks,
	},
}
</script>