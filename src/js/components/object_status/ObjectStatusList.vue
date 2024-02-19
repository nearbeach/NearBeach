<template>
	<div class="card">
		<div class="card-body">
			<h1>Object Status List</h1>
			<hr>

			<div class="row">
				<div class="col-md-4">
					<strong>Object Status List</strong>
					<p class="text-instructions">
						Click on any of the objects to edit the status' for that particular object.
					</p>
				</div>
				<div class="col-md-8 d-grid gap-2 mx-auto">
					<a v-bind:href="`${rootUrl}object_status_information/requirement/`"
					   class="btn btn-outline-primary"
					>
						Requirements
					</a>
					<a v-bind:href="`${rootUrl}object_status_information/requirement_item/`"
					   class="btn btn-outline-warning"
					>
						Requirement Item
					</a>
					<a v-bind:href="`${rootUrl}object_status_information/project/`"
					   class="btn btn-outline-success"
					>
						Projects
					</a>
					<a v-bind:href="`${rootUrl}object_status_information/task/`"
					   class="btn btn-outline-info"
					>
						Tasks
					</a>
				</div>
			</div>
		</div>
	</div>
</template>
<script>
import { mapGetters } from "vuex";

export default {
	name: "ObjectStatusList",
	props: {
		theme: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
}
</script>