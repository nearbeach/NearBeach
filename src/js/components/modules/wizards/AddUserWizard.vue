<template>
	<div
		class="modal fade"
		id="addUserModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Add User Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addUserCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div
						v-if="userFixList.length > 0"
						class="row"
					>
						<div class="col-md-4">
							<strong>Add Users</strong>
							<p class="text-instructions">
								Use the following multiple select to select
								which users you want to add to this
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
								:options="userFixList"
								v-model:value="userModel"
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
								<li>There are no more users left to add</li>
								<li>
									The user you are after is in a group not
									current added to this {{ destination }}
								</li>
							</ul>
						</div>
						<div class="col-md-6 no-search">
							<img
								v-bind:src="`${staticURL}NearBeach/images/placeholder/questions.svg`"
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
						v-bind:disabled="userModel.length === 0"
						v-on:click="addUser"
					>
						Add User(s)
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
	name: "AddUserWizard",
	components: {
		NSelect,
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			potentialUserList: "getPotentialUserList",
			rootUrl: "getRootUrl",
			staticURL: "getStaticUrl",
			userLevel: "getUserLevel",
		}),
	},
	data() {
		return {
			userFixList: [],
			userModel: [],
		};
	},
	watch: {
		potentialUserList(new_value) {
			if (new_value === undefined) return;

			this.userFixList = new_value.map(row => {
				return {
					value: row.id,
					label: `${row.username}: ${row.first_name} ${row.last_name}`,
				}
			})
		}
	},
	methods: {
		addUser() {
			//Update user about adding user
			this.$store.commit("updateAddingUserStatus", {
				addingUserStatus: true
			});

			//Construct the data_to_send array
			const data_to_send = new FormData();

			//Look through all of the results in user model and append
			this.userModel.forEach((row) => {
				data_to_send.append("user_list", row);
			});

			//User axios to send the data to the backend
			this.axios
				.post(
					`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_user/`,
					data_to_send
				)
				.then((response) => {
					//Close the modal
					document.getElementById("addUserCloseButton").click();

					//Clear the models
					this.userModel = [];

					//Update VueX with the required data
					this.$store.commit("updateGroupsAndUsers", {
						objectGroupList: response.data.object_group_list,
						objectUserList: response.data.object_user_list,
						potentialGroupList: response.data.potential_group_list,
						potentialUserList: response.data.potential_user_list,
						userGroupList: response.data.user_group_list,
					});

					//User has been added - return to false
					this.$store.commit("updateAddingUserStatus", {
						addingUserStatus: false,
					});
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Failed to add user",
						message: `Failed to add user. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
		},
	},
};
</script>


