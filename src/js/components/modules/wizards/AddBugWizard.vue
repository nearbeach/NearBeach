<template>
	<div
		class="modal fade"
		id="addBugModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-xl modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.usersIcon"></Icon>
						Add Bugs
						Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addBugsCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Adding Bugs</strong>
							<p class="text-instructions">
								Select which bug client you want to search data
								from. Then use keywords or bug id to search for
								the required bugs. Once the search results
								appear, select those appropriate bugs that you
								want to link to the {{ destination }}.
							</p>
						</div>
						<div class="col-md-8">
							<!-- Bug Client List -->
							<div class="form-group">
								<label>Bug Client</label>
								<n-select
									:options="bugClientList"
									label="bug_client_name"
									:option="'bug_client_id'"
									v-model:value="bugClientModel"
								></n-select>
							</div>
							<br/>

							<!-- Search Keywords -->
							<div class="form-group">
								<label>Search Keywords</label>
								<input
									type="text"
									v-model="searchModel"
									class="form-control"
									v-bind:disabled="bugClientModel == ''"
									v-on:keydown="startSearchTimer"
									maxlength="50"
								/>
							</div>
							<br/>

							<!-- The Search Results -->
							<div
								v-if="searchOn"
								class="no-search"
							>
								<strong>Currently Searching for Bugs</strong
								><br/>
								<img
									:src="`${staticUrl}/NearBeach/images/placeholder/online_connection.svg`"
									alt="Placeholder Search Image"
								/>
							</div>
							<div
								v-else-if="bugResults.length == 0"
								class="no-search"
							>
								<strong>No Search Results Sorry</strong><br/>
								<img
									:src="`${staticUrl}/NearBeach/images/placeholder/road_to_knowledge.svg`"
									alt="Placeholder Search Image"
								/>
							</div>
							<div
								v-else
								id="bug_results_div"
							>
								<table class="table">
									<thead>
									<tr>
										<td></td>
										<td>Bug Description</td>
										<td>Bug Status</td>
									</tr>
									</thead>
									<tbody>
									<tr
										v-for="bug in bugResults"
										:key="bug.id"
									>
										<td v-bind:id="`bug_no_${bug.id}`">
											<a
												href="javascript:void(0)"
												v-on:click="
														submitBug(bug.id)
													"
											>
												Add Bug
											</a>
										</td>
										<td>
											{{ bug.summary }}
											<div class="spacer"></div>
											<p class="small-text">
												Assigned to:
												{{ bug.assigned_to }}
											</p>
											<p class="small-text">
												Bug No. {{ bug.id }} |
												Priority. {{ bug.priority }}
											</p>
										</td>
										<td>{{ bug.status }}</td>
									</tr>
									</tbody>
								</table>
							</div>
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
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//JavaScript extras
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "AddBugWizard",
	components: {
		Icon,
		NSelect,
	},
	props: {
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
		}),
	},
	mixins: [iconMixin],
	data() {
		return {
			bugClientModel: "",
			bugClientList: [],
			bugResults: [],
			searchModel: "",
			searchOn: false,
			searchTimer: "",
		};
	},
	methods: {
		loadBugClientList() {
			this.axios.post(
				`${this.rootUrl}object_data/bug_client_list/`
			).then((response) => {
				//Clear out the bug list
				this.bugClientList = response.data.map((row) => {
					return {
						value: row.pk,
						label: row.fields.bug_client_name,
					};
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error loading bug client list",
					message: `We had an issue loading the bug client list - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		startSearchTimer() {
			//Destroy the first timer if it exists
			if (this.searchTimer !== "") {
				clearTimeout(this.searchTimer);
			}

			//Reset the timer
			this.searchTimer = setTimeout(() => {
				this.startSearch();
			}, 700);
		},
		startSearch() {
			//Escape conditions
			if (this.searchModel === "") {
				return;
			}

			//We want to tell the user that we are actually searching
			this.searchOn = true;

			//Prepare for the data we are sending
			const data_to_send = new FormData();
			data_to_send.set("bug_client_id", this.bugClientModel);
			data_to_send.set("search", this.searchModel);

			//Send the data - then wait for a response
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/query_bug_client/`,
				data_to_send
			).then((response) => {
				//Update the bug results
				this.bugResults = response.data;

				//Turn off the search
				this.searchOn = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Search Failed",
					message: `Sorry, the search for bug client has failed. Errors -> ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
			});
		},
		submitBug(bug_id) {
			//Tell user you are adding the bug
			const add_bug_element = document.getElementById(
				`bug_no_${bug_id}`
			);
			add_bug_element.innerHTML = "Adding Bug";

			//Filter for the bug information out of the bugResults
			const filted_bug_results = this.bugResults.filter((row) => {
				return row.id == bug_id;

			});

			//Setup data
			const data_to_send = new FormData();
			data_to_send.set("bug_client", this.bugClientModel);
			data_to_send.set("bug_id", bug_id);
			data_to_send.set(
				"bug_description",
				filted_bug_results[0].summary
			);
			data_to_send.set("bug_status", filted_bug_results[0].status);

			//Send data to the backend
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_bug/`,
				data_to_send
			).then((response) => {
				//Send the updated bug list up
				this.$emit("append_bug_list", response.data);

				//Update the user that the bug has been added
				add_bug_element.innerHTML = "Done";
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Submit Bug Failed",
					message: `Sorry, the submitting the bug failed. Errors -> ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		//If the location is inside the array - don't bother getting the data
		const escape_array = ["requirement_item"];
		if (escape_array.indexOf(this.destination) >= 0) return;

		//Wait 200ms before getting data
		this.$nextTick(() => {
			this.loadBugClientList();
		});
	},
};
</script>

<style scoped></style>
