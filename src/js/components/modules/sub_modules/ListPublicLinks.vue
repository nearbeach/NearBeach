<template>
	<h2>Public Links</h2>
	<p class="text-instructions">
		The following will be public links you can send to clients. The links will contain certain information of the
		current object. i.e. it's status and description. Becareful who you send the links too!
	</p>

	<div v-if="isFetchingData"
		 class="alert alert-info"
	>Currently loading data...</div>
	<div v-if="isFetchingData === false && publicLinkResults.length === 0"
		 class="alert alert-info"
	>
		Sorry. There are no public links setup for this object.
	</div>
	<table v-else
		   class="table table-striped"
	>
		<thead>
			<tr>
				<td>Public Link</td>
				<td style="text-align:center;width:100px;">Is Active</td>
				<td v-if="userLevel > 1" style="width:10px;"></td>
			</tr>
		</thead>
		<tbody>
			<tr v-for="link in publicLinkResults"
				:key="link.public_link_id"
			>
				<td>
					<button type="button"
							class="btn btn-link"
							v-on:click="copyPublicLink(link.public_link_id)"
					>
						{{formatUrl(link.public_link_id)}}
					</button>
				</td>
				<td style="text-align: center">
					<input
						class="form-check-input"
						type="checkbox"
						v-bind:checked="link.public_link_is_active"
						v-bind:data-public-link-id="link.public_link_id"
						v-bind:disabled="userLevel<=1"
						v-on:change="updateIsActive"
					/>
				</td>
				<td v-if="userLevel > 1">
					<span class="remove-link">
						<Icon
							v-bind:icon="icons.trashCan"
							v-on:click="deletePublicLink(link.public_link_id)"
						/>
					</span>
				</td>
			</tr>
		</tbody>
	</table>
	<div class="row submit-row"
		 v-if="isReadOnly===false && userLevel > 1"
	>
		<div class="col-md-12">
			<button class="btn btn-primary save-changes"
					v-on:click="createPublicLink"
			>
				Create Public Link
			</button>
		</div>
	</div>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

//Icon
import {Icon} from "@iconify/vue";
import iconMixin from "../../../mixins/iconMixin";

export default {
	name: "ListPublicLinks",
	props: {
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		overrideDestination: {
			type: String,
			default: "",
		},
		overrideLocationId: {
			type: Number,
			default: 0,
		},
	},
	data() {
		return {
			isFetchingData: true,
			publicLinkResults: [],
		};
	},
	watch: {
		overrideLocationId() {
			this.getPublicLinks();
		},
	},
	components: {
		Icon,
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		})
	},
	mixins: [iconMixin],
	methods: {
		async copyPublicLink(public_link_id) {
			//Get the URL
			const url = `${window.location.origin}${this.rootUrl}public/${this.getDestination()}/${this.getLocationId()}/${public_link_id}/`

			//Copy to the clipboard
			try {
				await navigator.clipboard.writeText(url);

				//Notify the user
				this.$store.dispatch("newToast", {
					header: "Public Link Copied",
					message: "Public Link has successfully copied to the clipboard",
					extra_classes: "bg-success",
				});
			} catch(error) {
				this.$store.dispatch("newToast", {
					header: "Can not copy public link",
					message: "Sorry, we failed to copy the public link",
					extra_classes: "bg-danger",
					delay: 0,
				});
			}
		},
		createPublicLink() {
			//Inform user of creating new link
			this.$store.dispatch("newToast", {
				header: "Creating New Toast",
				message: "Please wait whilst we create the toast",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "create_public_link",
			});

			//Contact backend - get public link
			this.axios.post(
				`${this.rootUrl}public_data/${this.getDestination()}/${this.getLocationId()}/create/`,
			).then((response) => {
				//Inform user of success
				this.$store.dispatch("newToast", {
					header: "Successful new Public Link",
					message: "We have been able to create a new public link",
					extra_classes: "bg-success",
					unique_type: "create_public_link",
				});

				//Replace everything
				this.publicLinkResults = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not create new public link",
					message: `Sorry, we failed to create the new public link. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "create_public_link",
				});
			})
		},
		deletePublicLink(public_link_id) {
			//Construct data to send
			const data_to_send = new FormData();
			data_to_send.set("public_link_id", public_link_id);

			//Notify user we are deleting the data
			this.$store.dispatch("newToast", {
				header: "Deleting Public Link",
				message: "Deleting Public Link",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "public_link_delete",
			})

			//Use axios
			this.axios.post(
				`${this.rootUrl}public_data/${this.getDestination()}/${this.getLocationId()}/delete/`,
				data_to_send,
			).then(() => {
				//Remove the row
				this.publicLinkResults = this.publicLinkResults.filter((row) => {
					return row.public_link_id !== public_link_id;
				});

				this.$store.dispatch("newToast", {
					header: "Successfully Deleted Public Link",
					message: "Successfully Deleted Public Link",
					extra_classes: "bg-success",
					unique_type: "public_link_delete",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Deleting Public Link",
					message: `Error - could not delete link. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "public_link_delete",
				});
			});
		},
		formatUrl(public_link_id) {
			//Double check we are getting the correct URL
			if (public_link_id === "" || public_link_id === undefined) {
				return "Data error!";
			}

			//Trucate the UUID - so if someone is viewing the screen they don't get the key
			const trunc_link_id = public_link_id.slice(0,7);

			return `${window.location.origin}${this.rootUrl}public/${this.getDestination()}/${this.getLocationId()}/${trunc_link_id}...`
		},
		getDestination() {
			return this.overrideDestination !== "" ? this.overrideDestination : this.destination;
		},
		getLocationId() {
			//If there is an overrideDestination - we want to use the overrideLocationId
			return this.overrideDestination !== "" ? this.overrideLocationId : this.locationId;
		},
		getPublicLinks() {
			//Escape if there is no location id
			if (this.getLocationId() === 0) return;

			this.axios(
				`${this.rootUrl}public_data/${this.getDestination()}/${this.getLocationId()}/get_links/`,
			).then((response) => {
				//Set the data
				this.publicLinkResults = response.data;

				//Set the fetch status to false
				this.isFetchingData = false;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error fetching Public Links",
					message: `We had an issue fetching the public links for this object. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateIsActive(event) {
			//Get the uuid
			const uuid = event.target.dataset.publicLinkId;

			//Tell the user we are updating the stats
			this.$store.dispatch("newToast", {
				header: "Updating Active Status for Private Link",
				message: "Please wait - we are updating the status",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: `is_active-${uuid}`,
			});

			//Translate the checked box
			let is_active = "False";
			if (event.target.checked) {
				is_active = "True";
			}

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("public_link_id", uuid);
			data_to_send.set("public_link_is_active", is_active);

			this.axios.post(
				`${this.rootUrl}public_data/${this.destination}/${this.locationId}/update_link/`,
				data_to_send,
			).then(() => {
				//Update user
				this.$store.dispatch("newToast", {
					header: "Successfully Updated",
					message: "We have updated the is active status for the link",
					extra_classes: "bg-success",
					unique_type: `is_active-${uuid}`,
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Active Status for Private Link",
					message: `We are sorry, something went wrong. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: `is_active-${uuid}`,
				});
			})
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.getPublicLinks();
		})
	},
}
</script>