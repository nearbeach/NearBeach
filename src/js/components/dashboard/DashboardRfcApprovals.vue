<template>
	<div
		v-if="rfcApprovalsList.length > 0"
		class="card rfc-approvals-card"
	>
		<div class="card-body">
			<h1>Request for Changes Waiting for Approval</h1>
			<hr />

			<p class="text-instructions">
				The following Request for Changes, require you to action them.
				You can either approve or reject these Request for Changes.
			</p>

			<table class="table">
				<thead>
					<tr>
						<td width="75%">Request for Change</td>
						<td width="25%">Implementation Date</td>
					</tr>
				</thead>
				<tbody>
					<tr
						v-for="rfc in rfcApprovalsList"
						:key="rfc.pk"
						class="bg-white"
					>
						<td>
							<a
								v-bind:href="`${rootUrl}rfc_readonly/${rfc.pk}/`"
							>
								<p>{{ rfc.fields.rfc_title }}</p>
								<div class="spacer"></div>
								<p class="small-text">RFC{{ rfc.pk }}</p>
							</a>
						</td>
						<td>
							{{
								getNiceDate(
									rfc.fields.rfc_implementation_start_date
								)
							}}
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");

	//Import mixins
	import datetimeMixin from "../../mixins/datetimeMixin";
	import errorModalMixin from "../../mixins/errorModalMixin";

	export default {
		name: "DashboardRfcApprovals.vue",
		props: {
			rootUrl: {
				type: String,
				default: "/",
			},
		},
		data() {
			return {
				rfcApprovalsList: [],
			};
		},
		mixins: [datetimeMixin, errorModalMixin],
		methods: {
			getRfcApprovalsList: function () {
				//Use axios to get data
				axios
					.post(`${this.rootUrl}dashboard/get/rfc_approvals/`)
					.then((response) => {
						//Place the data into rfcApprovalsList
						this.rfcApprovalsList = response.data;
					})
					.catch((error) => {
						this.showErrorModal(error, "Dashboard", "");
					});
			},
		},
		mounted() {
			this.getRfcApprovalsList();
		},
	};
</script>

<style scoped></style>
