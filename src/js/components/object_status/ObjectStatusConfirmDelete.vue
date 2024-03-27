<template>
	<div
		class="modal fade"
		id="confirmStatusDeleteModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Confirm Deletion</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmStatusDeleteModalClose"
					></button>
				</div>
				<div class="modal-body">
					<!-- WARNING -->
					<div class="alert alert-warning">
						<h4>WARNING</h4>
						<p>
							This process can not be reversed. Deleting a status will remove it completely.
						</p>
						<p>
							All objects connected with this status will have to migrate to a new status. This is also
							permanent and can not be reversed.
						</p>
					</div>

					<div class="row">
						<p><strong>Status: </strong>{{ statusData.status }}</p>
						<p><strong>Higher Order Status: </strong>{{ statusData.higherOrderStatus }}</p>
					</div>

					<div class="spacer"></div>
					<div class="row">
						<p>Please select an appropriate status to migrate too.</p>
						<label><strong>New Status for the objects</strong></label>
						<n-select
							v-bind:options="newStatusList"
							v-model:value="migrationStatusIdModel"
							style="z-index: 9999"
							class="new-card-destination"
						></n-select>
					</div>
					<br/>
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
						v-on:click="deleteStatus"
						v-bind:disabled="this.migrationStatusIdModel === null || this.migrationStatusIdModel === ''"
					>
						Delete Status
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { NSelect } from "naive-ui";
import { mapGetters } from "vuex";

export default {
	name: "ObjectStatusConfirmDelete",
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
	data() {
		return {
			migrationStatusIdModel: "",
			newStatusList: [],
		}
	},
	watch: {
		statusId() {
			//Clear the model
			this.migrationStatusIdModel = "";

			//Status Id has been updated - time to update the list to exclude this number
			this.newStatusList = this.statusList.filter((row) => {
				return parseInt(row.status_id) !== parseInt(this.statusId);
			}).map((row) => {
				return {
					label: row.status,
					value: row.status_id,
				};
			});
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteStatus() {
			//Update users on the status
			this.$store.dispatch("newToast", {
				header: "Removing Status",
				message: "Please wait whilst we remove the status",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "remove_status",
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("status_id", `${this.statusId}`);
			data_to_send.set("migration_status_id", this.migrationStatusIdModel);

			//Use axios
			this.axios.post(
				`${this.rootUrl}object_status_information/${this.destination}/delete/`,
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Status Successfully Removed",
					message: "Status has been removed",
					extra_classes: "bg-success",
					unique_type: "remove_status",
				});

				//Update the parent
				this.$emit("delete_status");

				//Close the modal
				document.getElementById("confirmStatusDeleteModalClose").click();
			}).catch((error) => {
				//Notify the user of the error
				this.$store.dispatch("newToast", {
					header: "Error Removing Status",
					message: `Sorry, we could not remove the status. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "remove_status",
				});
			})
		},
	},
}
</script>