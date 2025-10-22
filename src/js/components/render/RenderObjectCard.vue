<template>
	<div class="object-card-list">
		<h2 v-if="importVariables.header !== ''">{{ importVariables.header }}</h2>
		<div
v-for="result in searchResults"
			 v-if="searchResults.length > 0"
			 :key="result.pk"
			 class="object-card"
		>
			<div class="object-card--detail">
				<a
:href="`${rootUrl}${tempTranslate(destination)}_information/${result[importVariables.id]}/`"
					:target="target"
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
				<a
:href="`${rootUrl}${destination}_information/${result[importVariables.id]}/`"
					:target="target"
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

		<!-- Loading state -->
		<div
v-if="searchResults.length === 0"
			 class="object-card"
		>
			<div class="object-card--detail">
				<p class="card-text placeholder-glow">
					<span class="placeholder col-1"></span>
				  	<span class="placeholder col-12"></span>
				</p>
			</div>
			<div class="object-card--status">
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

//Composables
import {useNiceDatetime} from "Composables/datetime/useNiceDatetime";

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
	methods: {
		useNiceDatetime,
		tempTranslate(destination) {
			if (destination === "kanban_board") {
				return "kanban";
			}

			return destination;
		}
	},
}
</script>
