<template>
	<div class="object-card-list">
		<h2>{{ importVariables.header }}</h2>
		<div
v-for="result in searchResults"
			 :key="result.pk"
			 class="object-card"
		>
			<div class="object-card--checkbox">
				<input
:id="`${modelTarget}_${result.pk}`"
					   v-model="checkboxModel"
					   type="checkbox"
					   :value="result.pk"
			    />
			</div>
			<div class="object-card--detail">
				<a
:href="`${rootUrl}${destination}_information/${result[importVariables.id]}/`"
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
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

//Composables
import {useNiceDatetime} from "Composables/datetime/useNiceDatetime";

export default {
	name: "RenderObjectCardCheckbox",
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
		modelTarget: {
			type: String,
			default: "",
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
	emits: ["update_checkbox_model"],
	data() {
		return {
			checkboxModel: [],
		}
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
	watch: {
		checkboxModel() {
			this.$emit("update_checkbox_model", {
				"modelTarget": this.modelTarget,
				"value": this.checkboxModel,
			})
		},
	},
	methods: {
		useNiceDatetime
	},
}
</script>
