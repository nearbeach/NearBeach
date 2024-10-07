<template>
	<div
		class="card submit-rfc-card"
		v-if="showApprovalButton"
	>
		<div class="card-body">
			<!-- TEXT -->
			<div class="row">
				<h2>Approval Process</h2>
				<hr/>

				<p class="text-instructions">
					Please read the complete process for this Request for
					Change. If you decided to approve, please click on the
					"Approve RFC" button. If you reject this Request for Change,
					please click on the "Reject RFC" button.
				</p>
			</div>

			<!-- BUTTONS -->
			<div class="row submit-row rfc-submit-row">
				<div class="col-md-12">
					<a
						href="javascript:void(0)"
						class="btn btn-primary"
						v-on:click="approveRfc"
					>Approve RFC</a
					>

					<a
						href="javascript:void(0)"
						class="btn btn-danger reject-rfc"
						v-on:click="rejectRfc"
					>REJECT RFC</a
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//VueX
import {mapGetters} from "vuex";

export default {
	name: "RfcApprovalButtons",
	props: {
		rfcResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		groupLeaderCount: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
		showApprovalButton() {
			// Only show this section when;
			// - RFC Status is waiting for approval
			// - User is a group leader (groupLeaderCount > 0)
			return (
				this.rfcResults[0].fields.rfc_status === 2 &&
				this.groupLeaderCount > 0
			);
		},
	},
	methods: {
		approveRfc() {
			//Send the approval signal to the backend
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "3"); //Value 2: Waiting for Approval

			this.sendStatus(data_to_send);
		},
		rejectRfc() {
			//Send the rejection signal to the backend
			const data_to_send = new FormData();
			data_to_send.set("rfc_status", "6"); //Value 2: Waiting for Approval

			this.sendStatus(data_to_send);
		},
		sendStatus(data_to_send) {
			//Open up the loading modal
			this.$store.dispatch("newToast", {
				header: "Updating Status",
				message: "Updating Status. Please wait.",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "send_status",
			});

			//Use axios to send the status update to the backend
			this.axios.post(
				`${this.rootUrl}rfc_information/${this.rfcResults[0].pk}/update_status/`,
				data_to_send
			).then(() => {
				//Reload the page to get redirected to the correct place
				window.location.reload(true);
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error updating status",
					message: `Sorry, we could not update the status. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "send_status",
				});
			});
		},
	},
};
</script>


