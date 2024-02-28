<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.bugIcon"></Icon>
			Bugs List
		</h2>
		<p class="text-instructions">
			The following is a list of bugs associated with this
			{{ destination }}
		</p>

		<!-- TABLE OF BUGS -->
		<div
			v-if="bugList.length === 0"
			class="spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no bugs associated with this {{ destination }}
			</div>
		</div>
		<div v-else>
			<table class="table">
				<thead>
				<tr>
					<td>Bug Description</td>
					<td>Status</td>
				</tr>
				</thead>
				<tbody>
				<tr
					v-for="bug in bugList"
					:key="bug.pk"
				>
					<td>
						<a
							v-bind:href="getBugHyperLink(bug)"
							rel="noopener noreferrer"
							target="_blank"
						>
							<p>
								{{ bug.bug_description }}
							</p>
							<div class="spacer"></div>
							<p class="small-text">
								Bug No. {{ bug.bug_code }} -
								{{ bug.bug_client__bug_client_name }}
							</p>
						</a>
					</td>
					<td>
						{{ bug.bug_status }}
						<span
							class="remove-link"
							v-if="userLevel >= 2"
						>
								<Icon
									v-bind:icon="icons.trashCan"
									v-on:click="removeBug(bug.bug_id)"
								/>
							</span>
					</td>
				</tr>
				</tbody>
			</table>
		</div>

		<!-- Add Bug Button -->
		<!-- TO DO - limit it to certain users -->
		<hr/>
		<div class="row submit-row">
			<div class="col-md-12">
				<button
					class="btn btn-primary save-changes"
					v-on:click="addNewBug"
					v-if="userLevel > 1"
				>
					Add Bug
				</button>
			</div>
		</div>

		<!-- Modals -->
		<add-bug-wizard
			v-bind:destination="destination"
			v-bind:location-id="locationId"
			v-on:append_bug_list="appendBugList($event)"
		></add-bug-wizard>
	</div>
</template>

<script>
//JavaScript components
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";
import AddBugWizard from "../wizards/AddBugWizard.vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "BugsModule",
	components: {
		AddBugWizard,
		Icon,
	},
	mixins: [iconMixin],
	data() {
		return {
			bugList: [],
		};
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			userLevel: "getUserLevel",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addNewBug() {
			const addBugModal = new Modal(
				document.getElementById("addBugModal")
			);
			addBugModal.show();
		},
		appendBugList(data) {
			//Create object for the data
			let data_object = data[0].fields;

			//Add the bug id
			data_object.bug_id = data[0].pk;

			//Append the data
			this.bugList.push(data_object);
		},
		getBugHyperLink(bug) {
			if (
				bug.bug_client__list_of_bug_client__bug_client_name ===
				"Bugzilla"
			) {
				return `${bug.bug_client__bug_client_url}/show_bug.cgi?id=${bug.bug_code}`;
			}
			return "javascript:void(0)";
		},
		getBugList() {
			//We don't need to get the bug list when destination is requirement_items
			if (this.destination === "requirement_item") {
				//Jet pack out of there
				return;
			}

			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/bug_list/`
			).then((response) => {
				//Clear the current list
				this.bugList = [];

				//Loop through the results, and push each rows into the array
				response.data.forEach((row) => {
					this.bugList.push(row);
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to get bug list",
					message: `Failed to get bug list. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		removeBug(bug_id) {
			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("bug_id", bug_id);

			//Use Axios to send data to backend
			this.axios.post(
				`${this.rootUrl}object_data/delete_bug/`,
				data_to_send
			).then(() => {
				//Remove the bug from the model
				this.bugList = this.bugList.filter((row) => {
					return row.bug_id !== bug_id;
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Removing Bug",
					message: `We had an issue removing the bug - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		//If the location is inside the array - don't bother getting the data
		const escape_array = ["requirement_item"];
		if (escape_array.indexOf(this.destination) >= 0) return;

		this.$nextTick(() => {
			this.getBugList();
		});
	},
};
</script>

<style scoped></style>
