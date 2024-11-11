<template>
	<div
		class="modal fade"
		id="addGroupModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add Group Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addGroupCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div
						v-if="groupFixList.length > 0"
						class="row"
					>
						<div class="col-md-4">
							<strong>Add Groups</strong>
							<p class="text-instructions">
								Use the following multiple select to select
								which groups you want to add to this
								{{ destination }}.
							</p>
							<p class="text-instructions">
								Please note: A user's group has to be added to
								the {{ destination }} before the user can be
								added.
							</p>
						</div>
						<div class="col-md-8">
							<n-select
								:options="groupFixList"
								v-model:value="groupModel"
								multiple
							></n-select>
						</div>
					</div>
					<div
						v-else
						class="row"
					>
						<div class="col-md-6">
							<strong>Sorry - no results</strong>
							<p class="text-instructions">
								This could be because
							</p>
							<ul class="text-instructions">
								<li>There are no more groups left to add</li>
							</ul>
						</div>
						<div class="col-md-6 no-search">
							<img
								v-bind:src="`${staticUrl}NearBeach/images/placeholder/questions.svg`"
								alt="Sorry - there are no results"
							/>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-bind:disabled="groupModel.length == 0"
						v-on:click="addGroup"
					>
						Add Group(s)
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "AddGroupWizard",
	components: {
		NSelect,
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			potentialGroupList: "getPotentialGroupList",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	watch: {
		potentialGroupList(new_value) {
			if (new_value === undefined) return;

			this.groupFixList = new_value.map(row => {
				return {
					value: row.group_id,
					label: row.group_name,
				}
			})
		}
	},
	data() {
		return {
			groupFixList: [],
			groupModel: [],
		};
	},
	methods: {
		addGroup() {
			//Tell user we are adding groups
			this.$store.commit("updateAddingGroupStatus", {
				addingGroupStatus: true,
			});

			//Send the database the new groups to add
			const data_to_send = new FormData();

			//Loop through the model and append the results
			this.groupModel.forEach((row) => {
				data_to_send.append("group_list", row);
			});

			//user axios
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_group/`,
				data_to_send
			).then((response) => {
				//Update VueX with the required data
				this.$store.commit("updateGroupsAndUsers", {
					objectGroupList: response.data.object_group_list,
					objectUserList: response.data.object_user_list,
					potentialGroupList: response.data.potential_group_list,
					potentialUserList: response.data.potential_user_list,
					userGroupList: response.data.user_group_list,
				})

				//Update the user
				this.$store.commit("updateAddingGroupStatus", {
					addingGroupStatus: false,
				});

				//Clear the list
				this.groupModel = [];

				//Close this modal
				document.getElementById("addGroupCloseButton").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: `Error adding group to ${this.destination}`,
					message: `Sorry, we could not add the group to the ${this.destination}. Error -> ${error}`,
					extra_classes: "bd-danger",
					delay: 0,
				});
			});
		},
	},
};
</script>


