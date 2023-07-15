<template>
	<div
		class="modal fade"
		id="addGroupModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-lg">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.groupPresentation"></Icon> Add
						Group Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addGroupCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div
						v-if="groupFixList.length > 0"
						class="row"
					>
						<div class="col-md-4">
							<strong>Add Groups</strong>
							<p class="text-instructions">
								Use the following multiple select to select
								which groups you want to add to this
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
								:options="groupFixList"
								v-model:value="groupModel"
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
								<li>There are no more groups left to add</li>
							</ul>
						</div>
						<div class="col-md-6 no-search">
							<img
								v-bind:src="`${staticUrl}NearBeach/images/placeholder/questions.svg`"
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
						v-bind:disabled="groupModel.length == 0"
						v-on:click="addGroup"
					>
						Add Group(s)
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import { Icon } from "@iconify/vue";
	import { NSelect } from "naive-ui";

	//Mixins
	import errorModalMixin from "../../../mixins/errorModalMixin";
	import iconMixin from "../../../mixins/iconMixin";

	const axios = require("axios");

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "AddGroupWizard",
		components: {
			Icon,
			NSelect,
		},
		inject: [
			'nextTick',
		],
		computed: {
			...mapGetters({
				destination: "getDestination",
				locationId: "getLocationId",
				rootUrl: "getRootUrl",
				staticUrl: "getStaticUrl",
			}),
		},
		mixins: [errorModalMixin, iconMixin],
		data() {
			return {
				groupFixList: [],
				groupModel: [],
			};
		},
		methods: {
			addGroup() {
				//Send the database the new groups to add
				//Get the data_to_send ready
				const data_to_send = new FormData();

				//Loop through the model and append the results
				this.groupModel.forEach((row) => {
					data_to_send.append("group_list", row);
				});

				//user axios
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_group/`,
						data_to_send
					)
					.then((response) => {
						//Send the data upstream
						this.$emit("update_group_list", response.data);

						//Close this modal
						document.getElementById("addGroupCloseButton").click();

						//Get a new group list
						this.getGroupList();
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
			getGroupList() {
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/group_list_all/`
					)
					.then((response) => {
						//Clear the groupFixList
						this.groupFixList = response.data.map((row) => {
							return {
								value: row.pk,
								label: row.fields.group_name,
							};
						});
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
		},
		mounted() {
			//Wait 200ms
			this.nextTick(() => {
				this.getGroupList();
			});
		},
	};
</script>

<style scoped></style>
