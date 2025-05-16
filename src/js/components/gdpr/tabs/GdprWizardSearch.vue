<template>
	<div class="row">
		<div class="col-md-4">
			<strong>Search</strong>
			<p class="text-instructions">
				Search for the {{ gdprObjectType }} you wish to remove from NearBeach's data. Please note we can only focus
				on one objects at a time.
			</p>
		</div>
		<div class="col-md-8">
			<div class="form-group">
				<label>Search {{ gdprObjectType }}</label>
				<n-select
					:options="searchObjects"
					:placeholder="`Please search for a ${ gdprObjectType}`"
					v-model:value="searchResults"
					filterable
				/>
			</div>
		</div>
	</div>
</template>

<script>
import { NSelect } from "naive-ui";

//VueX
import { mapGetters } from "vuex";
export default {
	name: "GdprWizardSearch",
	components: {
		NSelect,
	},
	data() {
		return {
			searchObjects: [],
			searchResults: "",
		};
	},
	computed: {
		...mapGetters({
			gdprObjectType: "getGdprObjectType",
			rootUrl: "getRootUrl",
		}),
	},
	watch: {
		gdprObjectType() {
			if (this.gdprObjectType === "" || this.gdprObjectType === null) {
				//Empty object type, clear search data
				this.searchObjects = [];
				return;
			}

			//Fetch the data we want
			this.getSearchObjects();
		},
		searchResults() {
			this.$store.dispatch("processGdprObjectId", {
				"gdprObjectId": this.searchResults,
			});
		},
	},
	methods: {
		getSearchObjects() {
			// If there is no object type, we don't get any data
			if (this.gdprObjectType === "" || this.gdprObjectType === null) return;

			//Data to send
			const data_to_send = new FormData();
			data_to_send.set("gdpr_object_type", this.gdprObjectType);

			//AJAX CALL
			this.axios.post(
				`${this.rootUrl}gdpr_wizard/search_data/`,
				data_to_send,
			).then(response => {
				this.searchObjects = response.data;
			}).catch(error => {
				this.$store.dispatch("newToast", {
					header: "Can not fetch search data",
					message: `Can not fetch search data. ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			})
		},
	}

}
</script>