<template>
	<div
		id="confirmUserJobDeleteModal"
		class="modal fade"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmUserJobDelete"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						id="confirmUserJobDelete"
						class="modal-title"
					>
						Please confirm User Job Deletion
					</h5>
					<button
						id="confirmUserJobDeleteButton"
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to remove the current object from your planner?
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						@click="closeModal"
					>
						No
					</button>
					<button
						type="button"
						class="btn btn-primary"
						@click="deleteUserJob"
					>
						Yes
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {mapGetters} from "vuex";

export default {
	name: "ConfirmUserJobDelete",
	props: {
		userJobId: {
			type: Number,
			default: 0,
		},
	},
	emits: [
		'remove_user_job'
	],
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		})
	},
	methods: {
		deleteUserJob() {
			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set("user_job_id", `${this.userJobId}`);

			//Tell the backend to remove this group
			this.axios.post(
				`${this.rootUrl}my_planner/delete_user_job/`,
				data_to_send
			).then(() => {
				//Notify upstream we are deleting the id
				this.$emit("remove_user_job", {});
			})
			.catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error removing user job from my planner",
					message: `We encounted an error removing user job from the planner. Error -> ${error}`,
					extra_classes: 'bg-danger',
					delay: 0,
				});
			});

			//Close the modal
			this.closeModal();
		},
		closeModal() {
			document.getElementById("confirmUserJobDeleteButton").click();
		}
	},
}
</script>
