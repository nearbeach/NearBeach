<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1 class="mb-4">Group Information</h1>
				<a v-bind:href="`${this.rootUrl}search/group/`"
				>Back to group list</a
				>
				<hr/>

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
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button
							class="btn btn-danger"
							v-on:click="confirmDelete"
							v-if="parseInt(groupResults[0].pk) !== 1"
						>
							Delete Group
						</button>
						<button
							class="btn btn-primary save-changes"
							v-on:click="updateGroup"
						>
							Update Group
						</button>
					</div>
				</div>
			</div>
		</div>

		<confirm-group-delete
			v-bind:group-id="groupResults[0].pk"
		></confirm-group-delete>
	</n-config-provider>
</template>

<script>
import { NSelect, NConfigProvider } from "naive-ui";
import { Modal } from "bootstrap";

//Components
import ConfirmGroupDelete from "./ConfirmGroupDelete.vue";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "GroupInformation",
	components: {
		ConfirmGroupDelete,
		NConfigProvider,
		NSelect,
	},
	props: {
		groupResults: {
			type: Array,
			default() {
				return [];
			},
		},
		parentGroupResults: {
			type: Array,
			default() {
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
			groupNameModel: this.groupResults[0].fields.group_name,
			parentGroupFixList: [],
			parentGroupModel: this.groupResults[0].fields.parent_group,
		}
	},
	methods: {
		useNBTheme,
		confirmDelete() {
			//Show the modal
			const modal = new Modal(document.getElementById("confirmGroupDeleteModal"));
			modal.show();
		},
		updateGroup() {
			//Construct data to send
			const data_to_send = new FormData();
			data_to_send.set("group_name", this.groupNameModel);

			//Send parent group if not null
			if (this.parentGroupModel !== null && this.parentGroupModel !== "") {
				data_to_send.set("parent_group", this.parentGroupModel);
			}

			this.$store.dispatch("newToast", {
				header: "Updated Group",
				message: "Updated Group. Please wait.",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "update_group_leader",
			});

			//User axios to send data
			this.axios.post(
				`${this.rootUrl}group_information/${this.groupResults[0].pk}/save/`,
				data_to_send
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Group",
					message: "Successfully Update Group",
					extra_classes: "bg-success",
					delay: 0,
					unique_type: "update_group_leader",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Group",
					message: `We had an issue updating group. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "update_group_leader",
				});
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
		this.$store.commit({
			type: "updateTitle",
			title: this.groupNameModel,
		});
	},
};
</script>


