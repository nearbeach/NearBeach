<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>{{ nearbeachTitle }}</h1>
				<br/>
				<a :href="`${rootUrl}object_status_list/`">
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
							v-if="localStatusList.length === 0"
							class="error"
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
									:key="element.status_id"
									class="sortable"
									:data-id="element.status_id"
									@dblclick="editStatus($event)"
								>
									<div
:key="element.status_id"
										 class="content"
										 :data-id="element.status_id"
									>
										<strong
											:key="element.status_id"
											:data-id="element.status_id"
										>
											{{ element.status }}
										</strong>
									</div>
									<div
v-if="localStatusList.length > 1"
										 class="icon"
										 @click="removeStatus(element.status_id)"
									>
										<carbon-close-outline></carbon-close-outline>
									</div>
								</div>
							</template>
						</draggable>

						<div class="spacer"></div>

						<button
class="btn btn-primary"
								@click="newStatus"
						>
							New Status
						</button>
					</div>
				</div>
			</div>
		</div>

		<object-status-modal
			:status-data="statusData"
			:status-id="statusId"
			:status-list="localStatusList"
			@add_status="addStatus($event)"
			@update_status="updateStatus($event)"
		></object-status-modal>

		<object-status-confirm-delete
			:status-data="statusData"
			:status-id="statusId"
			:status-list="localStatusList"
			@delete_status="delete_status"
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
import {useNBTheme} from "Composables/theme/useNBTheme";

export default {
	name: "ObjectStatusInformation",
	components: {
		CarbonCloseOutline,
		draggable,
		ObjectStatusConfirmDelete,
		ObjectStatusModal,
	},
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
	}
}
</script>