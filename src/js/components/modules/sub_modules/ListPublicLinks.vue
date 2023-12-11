<template>
	<div v-if="isFetchingData"
		 class="alert alert-info"
	>Currently loading data...</div>
	<div v-if="isFetchingData === false && publicLinkResults.length === 0"
		 class="alert alert-info"
	>
		Sorry. There are no public links setup for this object.
	</div>
	<table v-else>
		<thead>
			<tr>
				<td>Public Link</td>
				<td>Is Active</td>
			</tr>
		</thead>
		<tbody>
			<tr v-for="link in publicLinkResults"
				:key="link.public_link_id"
			>
				<td>{{formatUrl(link.public_link_id)}}</td>
				<td style="text-align: center">
					<input
						class="form-check-input"
						type="checkbox"
						v-bind:checked="link.public_link_is_active"
						v-bind:data-public-link-id="link.public_link_id"
						v-on:change="updateIsActive"
					/>
				</td>

			</tr>
		</tbody>
	</table>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

export default {
	name: "ListPublicLinks",
	data() {
		return {
			isFetchingData: true,
			publicLinkResults: [],
		};
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		formatUrl(public_link_id) {
			//Double check we are getting the correct URL
			if (public_link_id === "" || public_link_id === undefined) {
				return "Data error!";
			}

			return `${this.rootUrl}public/${this.destination}/${this.locationId}/${public_link_id}/`
		},
		getPublicLinks() {
			this.axios(
				`${this.rootUrl}public_data/${this.destination}/${this.locationId}/get_links/`,
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
				extra_classes: "bg-warning",
				delay: 0,
				unique_type: `is_active-${uuid}`,
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("public_link_id", uuid);
			data_to_send.set("public_link_is_active", event.target.checked);

			this.axios.post(
				`${this.rootUrl}public_data/update_link/`,
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