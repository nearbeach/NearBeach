<template>
	<div>
		<h2>
			<Icon v-bind:icon="icons.linkOut"></Icon> {{ destination }} Links
		</h2>
		<p class="text-instructions">
			The following are links to other objects like
			projects/tasks/requirements. You can link a {{ destination }}
			to these other objects to symbolise a connection between the two.
		</p>

		<!-- OBJECT LINKS -->
		<div
			v-if="linkResults.length == 0"
			class="requirement-item-spacer"
		>
			<div class="alert alert-dark">
				Sorry - there are no Links for this requirement.
			</div>
		</div>
		<div v-else>
			<h3>Relates</h3>
			<div v-for="link in linkResults"
				 v-bind:key="link.pk"
			>
				<!-- Object ID + Title -->
				<div>
					<div>{{link.object_type}} - {{link.object_id}}</div>
					<div>{{link.object_title}}</div>
				</div>

				<!-- Object Status -->
				<div>
					{{link.object_status}}
					<span
						class="remove-link"
						v-if="userLevel >= 2"
					>
						<Icon
							v-bind:icon="icons.trashCan"
							v-on:click="removeLink(link)"
						/>
					</span>
				</div>
			</div>
		</div>

		<!-- Submit Button -->
		<div class="row submit-row">
			<div class="col-md-12">
				<a
					href="javascript:void(0)"
					class="btn btn-primary save-changes"
					v-on:click="newLink"
					v-if="userLevel > 1"
					>Create new Link</a
				>
			</div>
		</div>
		<hr />

		<!-- MODAL FOR NEW OBJECT LINKS -->
		<new-link-wizard
			v-bind:destination="destination"
			v-bind:location-id="locationId"
			v-on:update_link_results="updateLinkResults"
		></new-link-wizard>
	</div>
</template>

<script>
	import { Modal } from "bootstrap";
	import { Icon } from "@iconify/vue";
	import axios from "axios";
	import NewLinkWizard from "../wizards/NewLinkWizard.vue";

	//Mixins
	import iconMixin from "../../../mixins/iconMixin";

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "ObjectLinks",
		components: {
			Icon,
			NewLinkWizard,
		},
		mixins: [iconMixin],
		data() {
			return {
				linkResults: [],
			};
		},
		computed: {
			...mapGetters({
				destination: "getDestination",
				locationId: "getLocationId",
				rootUrl: "getRootUrl",
				userLevel: "getUserLevel",
			}),
		},
		methods: {
			newLink() {
				//Open up the modal

				var elem_modal = new Modal(
					document.getElementById("newLinkModal")
				);

				elem_modal.show();
			},
			removeLink(link) {
				//Get the data to send into the backend
				let data_to_send = new FormData();
				data_to_send.set("link_id", link.object_id);
				data_to_send.set("link_connection", link.object_type);

				//Send the data to the backend
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/remove_link/`,
						data_to_send
					)
					.then(() => {
						//Clear the data
						this.linkResults = [];

						//Update the data
						this.updateLinkResults();
					});
			},
			updateLinkResults() {
				//Get the data from the database
				axios
					.post(
						`${this.rootUrl}object_data/${this.destination}/${this.locationId}/object_link_list/`
					)
					.then((response) => {
						this.linkResults = response.data
					});
			},
		},
		mounted() {
			//Wait 200ms before getting data
			setTimeout(() => {
				this.updateLinkResults();
			}, 200);
		},
	};
</script>

<style scoped></style>
