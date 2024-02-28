<template>
	<div
		class="modal fade"
		id="updateChangeLeadModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
		v-if="userLevel > 1"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.userIcon"></Icon>
						Change Lead
						Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="updateChangeLeadCloseButton"
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
								:options="userFixList"
								v-model:value="userModel"
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
						v-bind:disabled="userModel.length === 0"
						v-on:click="changeLead"
					>
						Change Lead
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

export default {
	name: "UpdateChangeLeadWizard",
	components: {
		Icon,
		NSelect,
	},
	mixins: [iconMixin],
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

<style scoped></style>
