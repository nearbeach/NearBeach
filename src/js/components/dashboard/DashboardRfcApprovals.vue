<template>
	<div
		v-if="rfcApprovalsList.length > 0"
		class="card bg-danger"
	>
		<div class="card-body">
			<h1>Request for Changes Waiting for Approval</h1>
			<hr/>

			<p class="text-instructions">
				The following Request for Changes, require you to action them.
				You can either approve or reject these Request for Changes.
			</p>


			<render-object-card v-bind:search-results="rfcApprovalsList"
								v-bind:import-variables="rfcVariables"
								v-bind:destination="'rfc'"
			></render-object-card>
		</div>
	</div>
</template>

<script>
//Import mixins
import datetimeMixin from "../../mixins/datetimeMixin";
import RenderObjectCard from "../render/RenderObjectCard.vue";

export default {
	name: "DashboardRfcApprovals.vue",
	components: {RenderObjectCard},
	props: {
		rootUrl: {
			type: String,
			default: "/",
		},
	},
	data() {
		return {
			rfcApprovalsList: [],
			rfcVariables: {
				header: "Request for Change",
				prefix: "Rfc",
				id: "rfc_id",
				title: "rfc_title",
				status: "rfc_status__rfc_status",
			},
		};
	},
	mixins: [datetimeMixin],
	methods: {
		getRfcApprovalsList() {
			//Use axios to get data
			this.axios.post(
				`${this.rootUrl}dashboard/get/rfc_approvals/`
			).then((response) => {
				//Place the data into rfcApprovalsList
				this.rfcApprovalsList = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Getting RFC Approvals list",
					message: `We can not get the RFC Approvals List atm. Error -> ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		this.getRfcApprovalsList();
	},
};
</script>

<style scoped></style>
