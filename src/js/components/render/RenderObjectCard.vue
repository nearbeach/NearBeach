<template>
	<div class="object-card-list">
		<h2>{{ importVariables.header }}</h2>
		<div class="object-card"
			 v-for="result in searchResults"
			 :key="result.pk"
		>
			<div class="object-card--detail">
				<a v-bind:href="`${rootUrl}${destination}_information/${result[importVariables.id]}/`">
					<div class="object-card--detail--link">
						{{ importVariables.prefix }}{{ result[importVariables.id] }}
					</div>
					<div class="object-card--detail--description">
						{{ result[importVariables.title] }}
					</div>
				</a>
			</div>
			<div class="object-card--status">
				<div class="object-card--status--status">
					{{ result[importVariables.status] }}
				</div>
				<p class="small-text">
					{{ getNiceDatetime(result[importVariables.end_date]) }}
				</p>
			</div>
		</div>
	</div>
</template>

<script>
//Mixins
import datetimeMixin from "../../mixins/datetimeMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "RenderObjectCard",
	props: {
		destination: {
			type: String,
			default: "",
		},
		importVariables: {
			type: Object,
			default: () => {
				return {
					header: "",
					prefix: "",
					id: 0,
					title: "",
					status: "",
				};
			},
		},
		searchResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	mixins: [datetimeMixin],
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
}
</script>
