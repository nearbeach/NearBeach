<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Group</h1>
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Create a new group</strong>
						<p class="text-instructional">
							Each group should contain a unique name. If the name
							already exists then we won't be able to create the
							group.
						</p>
					</div>
					<div class="col-md-8">
						<div class="form-group">
							<label>
								Group Name
								<validation-rendering
									v-bind:error-list="v$.groupNameModel.$errors"
								></validation-rendering>
								<span
									class="error"
									v-if="!uniqueGroupName"
								>
								Please supply a unique name</span
								>
								<span
									class="error"
									v-if="checkingGroupName"
								>
								Checking group name...</span
								>
							</label>
							<input
								class="form-control"
								v-model="groupNameModel"
							/>
						</div>

						<div class="form-group">
							<label> Parent Group (optional) </label>
							<n-select
								:options="groupResultsFixList"
								v-model:value="parentGroupModel"
								label="group_name"
								class="form-control"
							/>
						</div>
					</div>
				</div>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<a
							href="javascript:void(0)"
							class="btn btn-primary save-changes"
							v-on:click="addNewGroup"
						>Create new Group</a
						>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NSelect} from "naive-ui";

// Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

// Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

export default {
	name: "NewGroup",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NSelect,
		ValidationRendering,
	},
	props: {
		groupResults: {
			type: Array,
			default() {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			checkingGroupName: false,
			groupNameModel: "",
			groupResultsFixList: [],
			parentGroupModel: "",
			searchTimeout: "",
			uniqueGroupName: true,
		};
	},
	mixins: [getThemeMixin],
	validations: {
		groupNameModel: {
			required,
		},
	},
	watch: {
		groupNameModel(new_value) {
			// Tell user that we are searching for the group name
			this.checkingGroupName = true;

			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (new_value.length >= 3) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.checkGroupName();
				}, 500);
			}
		},
	},
	methods: {
		addNewGroup() {
			//Check to make sure everything is validated
			this.v$.$touch();

			if (this.v$.$invalid || !this.uniqueGroupName) {
				//The group name is not valid, or is not unique. Show error and return
				this.$store.dispatch("newToast", {
					header: "Please check all fields",
					message: "Failed validation. Please check all fields are validated",
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_user",
				});

				//Just return
				return;
			}

			//Get the data
			const data_to_send = new FormData();
			data_to_send.set("group_name", this.groupNameModel);

			if (this.parentGroupModel !== undefined) {
				data_to_send.set("parent_group", this.parentGroupModel);
			}

			//Use Axios to send data
			this.axios.post(
				`${this.rootUrl}new_group/save/`, data_to_send
			).then((response) => {
				//Go to that webpage
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to Add New Group",
					message: `Sorry, could not save new group. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		checkGroupName() {
			//Send group name to backend to make sure it is not a duplicate
			const data_to_send = new FormData();
			data_to_send.set("search", this.groupNameModel);

			//User Axios to send data
			this.axios.post(
				`${this.rootUrl}group_information/check_group_name/`,
				data_to_send
			).then((response) => {
				// Update the uniqueGroupName
				this.uniqueGroupName = response.data.length === 0;

				// Hide the checking group name
				this.checkingGroupName = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to Check the Group Name",
					message: `Sorry, could not check the group name. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				})
			});
		},
	},
	mounted() {
		//This will map reconstruct the JSON data into a V-SELECT friendly data
		this.groupResultsFixList = this.groupResults.map((row) => {
			return {
				label: row.fields.group_name,
				value: row.pk,
			};
		});
	},
};
</script>

<style scoped></style>
