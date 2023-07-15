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
						<Icon v-bind:icon="icons.userIcon"></Icon> Add User
						Wizard
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
	import axios from "axios";
	import { Icon } from "@iconify/vue";
	import { NSelect } from "naive-ui";
	import { Modal } from "bootstrap";

	//VueX
	import { mapGetters } from "vuex";

	//Mixins
	import errorModalMixin from "../../../mixins/errorModalMixin";
	import iconMixin from "../../../mixins/iconMixin";

	export default {
		name: "AddUserWizard",
		components: {
			Icon,
			NSelect,
		},
		inject: [
			'nextTick',
		],
		props: {
			destination: {
				type: String,
				default: "",
			},
			locationId: {
				type: Number,
				default: 0,
			},
			refreshUserList: {
				type: Boolean,
				default: false,
			},
		},
		mixins: [errorModalMixin, iconMixin],
		computed: {
			...mapGetters({
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
		methods: {
			addUser() {
				//Construct the data_to_send array
				const data_to_send = new FormData();

				//Look through all of the results in user model and append
				this.userModel.forEach((row) => {
					data_to_send.append("user_list", row);
				});

				//User axios to send the data to the backend
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_user/`,
						data_to_send
					)
					.then((response) => {
						//Emit the data up
						this.$emit("update_user_list", response.data);

						//Close the modal
						document.getElementById("addUserCloseButton").click();

						//Clear the models
						this.userModel = [];

						//Update the list of users
						this.getUserList();

						//If kanban card - bring up card information again
						if (this.destination === "kanban_card") {
							//Send the data upstream
							this.$store.commit({
								type: "updateUserList",
								userList: response.data,
							});

							//Reshow the card information modal
							const cardModal = new Modal(
								document.getElementById("cardInformationModal")
							);
							cardModal.show();
						}
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			getUserList() {
				//If destination is '' or locationId = 0, there will be no information to get. Escape
				if (
					this.destination === "" ||
					this.locationId === 0 ||
					this.userLevel <= 1
				) {
					return;
				}

				//Setup the url
				let url = `${this.rootUrl}object_data/${this.destination}/${this.locationId}/user_list_all/`;

				//Use axios to obtain user lists
				axios.post(url).then((response) => {
					//Clear the user fix list
					this.userFixList = response.data.map((row) => {
						return {
							value: row.id,
							label: `${row.username}: ${row.first_name} ${row.last_name}`,
						};
					});
				});
			},
		},
		watch: {
			refreshUserList() {
				//Looks like the system has send the call function to reset the user list.
				if (this.refreshUserList) {
					this.getUserList();
				}

				//Turn it false again
				this.$emit("reset_refresh_user_list");
			},
		},
		mounted() {
			this.nextTick(() => {
				this.getUserList();
			});
		},
	};
</script>

<style scoped></style>
