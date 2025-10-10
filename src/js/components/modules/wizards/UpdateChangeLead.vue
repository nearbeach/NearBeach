<template>
	<div
		v-if="userLevel > 1"
		id="updateChangeLeadModal"
		class="modal fade"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						Change Lead Wizard
					</h2>
					<button
						id="updateChangeLeadCloseButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Change User</strong>
							<p class="text-instructions">
								Please use the dropdown to select the new
								Change User
							</p>
						</div>
						<div class="col-md-8">
							<n-select
								v-model:value="userModel"
								:options="userFixList"
							></n-select>
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
						:disabled="userModel.length === 0"
						@click="changeLead"
					>
						Change Lead
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
	name: "UpdateChangeLeadWizard",
	components: {
		NSelect,
	},
	emits: [
		'update_change_lead'
	],
	data() {
		return {
			userFixList: [],
			userModel: [],
		};
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
		changeLead() {
			//Construct the data_to_send array
			const data_to_send = new FormData();
			data_to_send.set("username", this.userModel);

			//User axios to send the data to the backend
			this.axios.post(
				`${this.rootUrl}rfc_information/${this.locationId}/update_change_lead/`,
				data_to_send
			).then((response) => {
				//Update the data
				this.$emit("update_change_lead", response.data.change_lead_results);

				//Close the modal
				document.getElementById("updateChangeLeadCloseButton").click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error changing the lead",
					message: `Sorry, we could not change the lead. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
};
</script>


