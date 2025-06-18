<template>
	<div class="object-card-list">
		<h2>{{ importVariables.header }}</h2>
		<div class="object-card"
			 v-for="result in searchResults"
			 :key="result.pk"
		>
			<div class="object-card--detail">
				<a v-bind:href="`${rootUrl}${tempTranslate(destination)}_information/${result[importVariables.id]}/`"
					v-bind:target="target"
				>
					<div class="object-card--detail--link">
						{{ importVariables.prefix }}{{ result[importVariables.id] }}
					</div>
					<div class="object-card--detail--description">
						{{ result[importVariables.title] }}
					</div>
				</a>
			</div>
			<div class="object-card--status">
				<a v-bind:href="`${rootUrl}${destination}_information/${result[importVariables.id]}/`"
					v-bind:target="target"
				>
					<div class="object-card--status--status">
						{{ result[importVariables.status] }}
					</div>
					<p class="small-text">
						{{ useNiceDatetime(result[importVariables.end_date]) }}
					</p>
				</a>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

//Composables
import {useNiceDatetime} from "../../composables/datetime/useNiceDatetime";

export default {
	name: "RenderObjectCard",
	methods: {
		useNiceDatetime,
		tempTranslate(destination) {
			if (destination === "kanban_board") {
				return "kanban";
			}

			return destination;
		}
	},
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
		target: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
}
</script>
