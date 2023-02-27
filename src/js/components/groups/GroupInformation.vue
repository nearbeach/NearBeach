<template>
	<div class="card">
		<div class="card-body">
			<h1>Group Information</h1>
			<br />
			<a v-bind:href="`${this.rootUrl}search/group/`"
				>Back to group list</a
			>
			<hr />

			<div class="row">
				<div class="col-md-4">
					<strong>Group Information</strong>
					<p class="text-instruction">
						Please edit the group information here. Please note -
						groups have to be unique!
					</p>
				</div>
				<div class="col-md-8">
					<div class="form-group">
						<label>Group Name</label>
						<input
							type="text"
							v-model="groupNameModel"
							class="form-control"
						/>
					</div>
					<div class="form-group">
						<label>Parent Group</label>
						<n-select
							v-model:value="parentGroupModel"
							filterable
							:options="parentGroupFixList"
							clearable
						/>
					</div>
				</div>
			</div>

			<!-- Submit Button -->
			<hr />
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						href="javascript:void(0)"
						class="btn btn-primary save-changes"
						v-on:click="updateGroup"
						>Update Group</a
					>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	const axios = require("axios");
	import { NSelect } from "naive-ui";

	//Load mixins
	import errorModalMixin from "../../mixins/errorModalMixin";
	import loadingModalMixin from "../../mixins/loadingModalMixin";

	export default {
		name: "GroupInformation",
		components: {
			NSelect,
		},
		props: {
			groupResults: {
				type: Array,
				default: function () {
					return [];
				},
			},
			parentGroupResults: {
				type: Array,
				default: function () {
					return [];
				},
			},
			rootUrl: {
				type: String,
				default: "/",
			},
		},
		data() {
			return {
				groupNameModel: this.groupResults[0].fields.group_name,
				parentGroupFixList: [],
				parentGroupModel: this.groupResults[0].fields.parent_group,
			};
		},
		mixins: [errorModalMixin, loadingModalMixin],
		methods: {
			updateGroup: function () {
				//Construct data to send
				const data_to_send = new FormData();
				data_to_send.set("group_name", this.groupNameModel);
				data_to_send.set("parent_group", this.parentGroupModel);

				//Show the loading mixin
				this.showLoadingModal("Group Information");

				//User axios to send data
				axios
					.post(
						`${this.rootUrl}group_information/${this.groupResults[0].pk}/save/`,
						data_to_send
					)
					.then((response) => {
						this.closeLoadingModal();
					})
					.catch((error) => {
						this.showErrorModal(error, "group_information", "");
					});
			},
		},
		mounted() {
			// Create the parent group fix list
			const parent_group_fix_list = this.parentGroupResults.map((row) => {
				return {
					group_name: row.fields.group_name,
					label: row.fields.group_name,
					value: row.pk,
				};
			});

			//Set the variables
			this.parentGroupFixList = parent_group_fix_list;

			//Send the rootUrl to VueX
			this.$store.commit({
				type: "updateUrl",
				rootUrl: this.rootUrl,
			});
		},
	};
</script>

<style scoped></style>
