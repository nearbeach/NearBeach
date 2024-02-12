<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<list-public-links
					v-bind:is-read-only="isReadOnly"
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