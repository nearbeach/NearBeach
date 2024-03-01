<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<list-public-links
					v-bind:is-read-only="isReadOnly"
					v-bind:override-destination="'kanban_board'"
					v-bind:override-location-id="locationId"
				></list-public-links>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import getThemeMixins from "../../mixins/getThemeMixin"
import ListPublicLinks from "../modules/sub_modules/ListPublicLinks.vue"

export default {
	name: "KanbanPublicLinks",
	mixins: [getThemeMixins],
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