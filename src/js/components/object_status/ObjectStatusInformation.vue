<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>{{ nearbeachTitle }}</h1>
				<br/>
				<a v-bind:href="`${this.rootUrl}object_status_list/`">
					Go back to object status list
				</a>
				<hr>

				<div class="row">
					<div class="col-md-4">
						<strong>Editing Status</strong>
						<p class="text-instructions">
							Move the status' around to reorder them. Double click to edit text and settings.
						</p>
					</div>
					<div class="col-md-8">
						<strong>Status List</strong>
						<span
							class="error"
							v-if="localStatusList.length === 0"
						>
							Please create at least one status
						</span>
						<br/>
						<draggable
							v-model="localStatusList"
							item-key="status_id"
							ghost-class="ghost"
							@change="updateSortOrder"
						>
							<template
								#item="{ element }"
								type="transition"
								name="flip-list"
							>
								<div
									class="sortable"
									v-bind:key="element.status_id"
									v-bind:data-id="element.status_id"
									v-on:dblclick="editStatus($event)"
								>
									<div class="content"
										 v-bind:key="element.status_id"
										 v-bind:data-id="element.status_id"
									>
										<strong
											v-bind:key="element.status_id"
											v-bind:data-id="element.status_id"
										>
											{{ element.status }}
										</strong>
									</div>
									<div class="icon"
										 v-on:click="removeStatus(element.status_id)"
										 v-if="localStatusList.length > 1"
									>
										<carbon-close-outline></carbon-close-outline>
									</div>
								</div>
							</template>
						</draggable>

						<div class="spacer"></div>

						<button v-on:click="newStatus"
								class="btn btn-primary"
						>
							New Status
						</button>
					</div>
				</div>
			</div>
		</div>

		<object-status-modal
			v-bind:status-data="statusData"
			v-bind:status-id="statusId"
			v-bind:status-list="localStatusList"
			v-on:add_status="addStatus($event)"
			v-on:update_status="updateStatus($event)"
		></object-status-modal>

		<object-status-confirm-delete
			v-bind:status-data="statusData"
			v-bind:status-id="statusId"
			v-bind:status-list="localStatusList"
			v-on:delete_status="delete_status"
		></object-status-confirm-delete>
	</n-config-provider>
</template>

<script>
//Draggable
import draggable from "vuedraggable";

//Bootstrap
import { Modal } from "bootstrap";

//Components
import ObjectStatusConfirmDelete from "./ObjectStatusConfirmDelete.vue";
import ObjectStatusModal from "./ObjectStatusModal.vue";
import {CarbonCloseOutline} from "../../components";
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "ObjectStatusInformation",
	props: {
		destination: {
			type: String,
			default: "",
		},
		nearbeachTitle: {
			type: String,
			default: "Status Editor",
		},
		objectStatusResults: {
			type: Array,
			default: () => {
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
	components: {
		CarbonCloseOutline,
		draggable,
		ObjectStatusConfirmDelete,
		ObjectStatusModal,
	},
	data() {
		return {
			localStatusList: this.objectStatusResults,
			statusData: {
				higherOrderStatus: "Closed",
				status: "",
			},
			statusId: 0,
		}
	},
	methods: {
		useNBTheme,
		addStatus(data) {
			//Add the data to the local status list
			this.localStatusList.push(data[0]);
		},
		delete_status() {
			//Just remove it from the local status list
			this.localStatusList = this.localStatusList.filter((row) => {
				return row.status_id !== this.statusId;
			});
		},
		editStatus(event) {
			
			//Get the id
			const status_id = parseInt(event.target.dataset.id);

			//Update props
			this.updateProps(status_id);

			//Open the modal
			const modal = new Modal(document.getElementById("objectStatusModal"));
			modal.show();
		},
		newStatus() {
			//Empty out the objectData
			this.statusData = {
				higherOrderStatus: "Normal",
				status: "",
			};

			//Update the status id
			this.statusId = 0;

			//Open Object Status Modal
			const modal = new Modal(document.getElementById("objectStatusModal"));
			modal.show();
		},
		removeStatus(status_id) {
			//Update the props
			this.updateProps(status_id);

			//Make modal appear
			const modal = new Modal(document.getElementById("confirmStatusDeleteModal"));
			modal.show();
		},
		updateProps(status_id) {
			//Filter for the required data
			const data = this.localStatusList.filter((row) => {
				return parseInt(row.status_id) === status_id;
			})

			//Check to make sure we have data
			if (data.length === 0) return;

			//Setup the object
			this.statusData = {
				higherOrderStatus: data[0].higher_order_status,
				status: data[0].status,
			};

			//Update the status id
			this.statusId = status_id;
		},
		updateSortOrder() {
			//Update user on status change
			this.$store.dispatch("newToast", {
				header: "Updating Sort Order",
				message: "Please wait, as we update the sort order",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "sort_order",
			});

			//Setup data_to_send
			const data_to_send = new FormData();

			//Loop through the local status' and get the status id
			this.localStatusList.forEach((row) => {
				data_to_send.append("status_id", row.status_id);
			});

			//Send data to backend
			this.axios.post(
				`${this.rootUrl}object_status_information/${this.destination}/reorder/`,
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Sort Order",
					message: "Sort Order has been updated",
					extra_classes: "bg-success",
					unique_type: "sort_order",
				});

				//Add Code
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed Updating Sort Order",
					message: `We've encounted an issue updating the sort order: Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "sort_order",
				});
			})
		},
		updateStatus(data) {
			//Get the status id for checking
			const status_id = parseInt(data.statusId);

			//Check to make sure there is no issue
			if (status_id === undefined) {
				this.$store.dispatch("newToast", {
					header: "Error updating card",
					message: "Please reload the page. We have experienced an in page issue",
					extra_classes: "bg-danger",
					delay: 0,
				});

				return;
			}

			//Get the index for the status location
			const index = this.localStatusList.findIndex(row => row.status_id === status_id);

			//Update that object
			this.localStatusList[index].higher_order_status = data.higherOrderStatus;
			this.localStatusList[index].status = data.status;
		}
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		this.$store.commit({
			type: "updateDestination",
			destination: this.destination,
		});
	}
}
</script>