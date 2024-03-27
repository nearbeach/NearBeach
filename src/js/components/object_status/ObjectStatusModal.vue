<template>
	<div
		class="modal fade"
		id="objectStatusModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
		data-bs-keyboard="false"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="exampleModalLabel"
					>
						Add/Edit Status
					</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="objectStatusModalClose"
					></button>
				</div>
				<div class="modal-body">
					<div class="form-group">
						<label>
							Status
							<span class="error"
								  v-if="isDuplicate"
							>
								Sorry, there is a status of that name already
							</span>
						</label>
						<input
							v-model="localStatusModel"
							type="text"
							class="form-control"
						/>
					</div>

					<div class="spacer"></div>

					<div class="form-group">
						<label>Higher Order Status</label>
						<n-select
							v-model:value="higherOrderStatusModel"
							:options="higherOrderStatusList"
						/>
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
						v-bind:disabled="isDuplicate"
						v-on:click="saveChanges"
					>
						Save changes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

//Components
import {NSelect} from "naive-ui";

export default {
	name: "ObjectStatusModal",
	components: {
		NSelect,
	},
	props: {
		statusData: {
			type: Object,
			default: () => {
				return {
					higherOrderStatus: "Closed",
					status: "",
				}
			},
		},
		statusId: {
			type: Number,
			default: 0,
		},
		statusList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			rootUrl: "getRootUrl",
		}),
	},
	data() {
		return {
			higherOrderStatusList: [
				{
          			label: 'Backlog',
          			value: 'Backlog'
				},
				{
					label: 'Blocked',
					value: 'Blocked'
				},
				{
					label: 'Normal',
					value: 'Normal'
				},
				{
					label: 'Closed',
					value: 'Closed'
				},
			],
			higherOrderStatusModel: "Normal",
			isDuplicate: false,
			localStatusModel: "",
		}
	},
	watch: {
		statusId() {
			//Status id has changed, update the local variables
			this.higherOrderStatusModel = this.statusData.higherOrderStatus;
			this.localStatusModel = this.statusData.status;
		},
		localStatusModel() {
			//Find out if there are any duplicates
			const count = this.statusList.filter((row) => {
				return row.status.toLowerCase() === this.localStatusModel.toLowerCase();
			}).length;

			this.isDuplicate = count > 0;
		}
	},
	methods: {
		editStatus() {
			//Notify the user of the status update
			this.$store.dispatch("newToast", {
				header: "Updating Status",
				message: "Please wait whilst we update the status",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "update_status",
			});

			//Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("status_id", this.statusId.toString());
			data_to_send.set("status", this.localStatusModel);
			data_to_send.set("higher_order_status", this.higherOrderStatusModel);

			//Use axios to send the data
			this.axios.post(
				`${this.rootUrl}object_status_information/${this.destination}/update/`,
				data_to_send,
			).then((response) => {
				this.$emit("update_status", {
					statusId: this.statusId,
					status: this.localStatusModel,
					higherOrderStatus: this.higherOrderStatusModel,
				});

				//Notify user of success
				this.$store.dispatch("newToast", {
					header: "Successfully updated status",
					message: "Status has been updated",
					extra_classes: "bg-success",
					unique_type: "update_status",
				});

				//Close modal
				document.getElementById("objectStatusModalClose").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error updating status",
					message: `Sorry, but we could not update your status. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_status",
				});
			});
		},
		newStatus() {
			//Tell users of the new status
			this.$store.dispatch("newToast", {
				header: "Creating New Status",
				message: "Please wait whilst we create new status",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "create_status",
			});

			//Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("status", this.localStatusModel);
			data_to_send.set("higher_order_status", this.higherOrderStatusModel);

			//Use axios to send the data
			this.axios.post(
				`${this.rootUrl}object_status_information/${this.destination}/create/`,
				data_to_send,
			).then((response) => {
				this.$store.dispatch("newToast", {
					header: "Created New Status",
					message: "New Status has been created successfully",
					extra_classes: "bg-success",
					unique_type: "create_status",
				});

				//Send this data upstream
				this.$emit("add_status", response.data);

				//Close modal
				document.getElementById("objectStatusModalClose").click();

				//Clear out the data
				this.localStatusModel = "";
				this.higherOrderStatusModel = "Normal";
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Creating New Status",
					message: `Sorry, we could not create the status. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "create_status",
				});

				//ADD CODE
			});
		},
		saveChanges() {
			//Depending on the status id, depends if it is new or existing
			if (parseInt(this.statusId) === 0) {
				this.newStatus();
			} else {
				this.editStatus();
			}
		},
	},
}
</script>