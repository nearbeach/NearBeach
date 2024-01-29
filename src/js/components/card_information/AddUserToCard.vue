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
						<Icon v-bind:icon="icons.userIcon"></Icon>
						Add User
						To Card
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
								kanban card.
							</p>
							<p class="text-instructions">
								Please note: A user's group has to be added to
								the kanban card before the user can be
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
									current added to this kanban card
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
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";
import {Modal} from "bootstrap";

//VueX
import {mapGetters} from "vuex";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "AddUserToCard",
	components: {
		Icon,
		NSelect,
	},
	mixins: [iconMixin],
	computed: {
		...mapGetters({
			cardId: "getCardId",
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
			//Construct the data_to_send array
			const data_to_send = new FormData();

			//Look through all of the results in user model and append
			this.userModel.forEach((row) => {
				data_to_send.append("user_list", row);
			});

			//User axios to send the data to the backend
			this.axios.post(
				`${this.rootUrl}object_data/kanban_card/${this.cardId}/add_user/`,
				data_to_send
			).then((response) => {
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
				})

				//Reshow the card information modal
				const cardModal = new Modal(
					document.getElementById("cardInformationModal")
				);
				cardModal.show();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error adding user to kanban card",
					message: `Sorry, we could not add the user to the kanban card. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
};
</script>

<style scoped></style>
