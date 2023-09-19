<template>
	<div
		class="modal fade"
		id="confirmChangeTaskClosure"
		tabindex="-1"
		data-bs-backdrop="static"
		data-bs-keyboard="false"
		aria-labelledby="confirmChangeTaskClosure"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5
						class="modal-title"
						id="confirmChangeTaskClosure"
					>
						Set Task to {{ closureStatus }}
					</h5>
					<!-- TASK INFORMATION -->
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="confirmChangeTaskCloseButton"
					></button>
				</div>
				<div class="modal-body">
					Are you sure you want to close the Change Task {{ closureId }} - with the status of
					{{ closureStatus }}?
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						v-on:click="closeModal"
					>
						No
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="closeChangeTask"
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
	name: "ConfirmChangeTaskClosure",
	props: {
		closureId: {
			type: Number,
			default: 0,
		},
		closureStatus: {
			type: String,
			default: "",
		},
		closureStatusId: {
			type: Number,
			default: 0,
		},
	},
	methods: {
		closeChangeTask() {
			//Emit the data upstream
			this.$emit("close_change_task", {
				closureId: this.closureId,
				closureStatusId: this.closureStatusId,
			});

			//Close the modal
			this.closeModal();
		},
		closeModal() {
			document.getElementById("confirmChangeTaskCloseButton").click();
		}
	},
}
</script>
