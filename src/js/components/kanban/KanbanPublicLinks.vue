<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<list-public-links></list-public-links>
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