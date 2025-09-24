<template>
	<div
		class="modal fade"
		id="confirmLinkDeleteModal"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmLinkDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmLinkDelete"
					>
						Please confirm Link Deletion
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmLinkDeleteButton"
					></button>
				</div>
				<div class="modal-body">
					<div class="row">
						<p>Are you sure you want to delete the link?</p>
					</div>
					<div class="row">
						<p>
							<strong>{{formatId(objectLink.object_type, objectLink.object_id)}}</strong><br/>
							<strong>Title: </strong>{{objectLink.object_title}}
						</p>
					</div>
					<div class="row mt-2"
						 v-if="objectLink.link_relationship.toLowerCase() === 'block'"
					>
						<p class="mb-0">
							Alternatively, for any Blocked links we can migrate them to the "Related" status.
						</p>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary me-auto"
						v-on:click="closeModal"
					>
						Cancel
					</button>
					<button
						v-if="objectLink.link_relationship.toLowerCase() === 'block' && showMigrateButton"
						type="button"
						class="btn btn-info"
						v-on:click="processLink('migrate')"
					>Migrate Link</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="processLink('remove')"
					>
						Delete Link
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
	name: "ConfirmLinkDelete",
	emits: [
		'update_link_results',
	],
	props: {
		showMigrateButton: {
			type: Boolean,
			default: true,
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			objectLink: "getObjectLink",
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		closeModal() {
			document.getElementById("confirmLinkDeleteButton").click();
		},
		formatId(object_type, object_id) {
			switch (object_type) {
				case "project":
					return `Pro${object_id}`;
				case "requirement":
					return `Req${object_id}`;
				case "requirement_item":
					return `Item${object_id}`;
				case "task":
					return `Task${object_id}`;
				default:
					return `${object_type.slice(0,3)}${object_id}`;
			}
		},
		processLink(process) {
			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set("link_id", this.objectLink.object_id);
			data_to_send.set(
				"link_connection",
				this.objectLink.object_type === this.destination ? "meta_object" : this.objectLink.object_type
			);

			//Send the data to the backend
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/${process}_link/`,
				data_to_send
			).then(() => {
				//Update the data
				this.$emit("update_link_results", {});
			});

			//Close the modal
			this.closeModal();
		},
	},
}
</script>
