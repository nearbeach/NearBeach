<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Stakeholder Organisation</h2>
			<p class="text-instructions">
				Please search for your stakeholder's organisation in the
				dropdown box. Once found, please select.
			</p>
			<p class="text-instructions">
				If you can not find your organisation, please
				<a v-bind:href="`${rootUrl}new_organisation/`" target="_blank" rel="noopener noreferrer" >
					click here to create it.
				</a>
				Then search for it again
			</p>
		</div>
		<div class="col-md-8">
			<div class="form-group">
				<label
				>Stakeholder Organisation
					<validation-rendering
						v-bind:error-list="v$.stakeholderModel.$errors"
					></validation-rendering>
				</label>
				<n-select
					:options="stakeholderFixList"
					filterable
					placeholder="Search Stakeholders"
					@search="fetchOptions"
					v-model:value="stakeholderModel"
					label="organisation_name"
					class="get-stakeholders"
				/>
			</div>
		</div>
	</div>
</template>

<script>
//JavaScript Libraries
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "GetStakeholders",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NSelect,
		ValidationRendering,
	},
	emits: ['update_stakeholder_model'],
	props: {
	},
	data() {
		return {
			searchTimeout: "",
			stakeholderFixList: [],
			stakeholderModel: "",
		};
	},
	validations: {
		stakeholderModel: {
			required,
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		fetchOptions(search, loading) {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (search.length >= 3) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getOrganisationData(search, loading);
				}, 500);
			}
		},
		getOrganisationData(search) {
			// Save the seach data in FormData
			const data_to_send = new FormData();
			data_to_send.set("search", search);

			// Now that the timer has run out, lets use AJAX to get the organisations.
			this.axios.post(
				`${this.rootUrl}search/organisation/data/`,
				data_to_send
			).then((response) => {
				//Extract the required JSON data
				const extracted_data = response.data;

				//Look through the extracted data - and map the required fields into stakeholder fix list
				this.stakeholderFixList = extracted_data.map((row) => {
					//Create the creation object
					return {
						value: row.pk,
						label: row.fields.organisation_name,
					};
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting organisation data",
					message: `Error getting the organisation data. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				})
			});
		},
	},
	watch: {
		stakeholderModel() {
			//Send the changes upstream
			this.$emit("update_stakeholder_model", this.stakeholderModel);
		},
	},
	mounted() {
		this.$nextTick(() => {
			//Get a default list when mounted
			this.getOrganisationData("", "");
		});
	},
};
</script>


