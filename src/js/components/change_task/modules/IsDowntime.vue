<template>
	<div class="row">
		<div class="col-md-4">
			<strong>Misc</strong>
			<p class="text-instructions">
				To state if there is downtime, please click the "No
				Downtime" to change it's statue.
			</p>
			<p class="text-instructions">
				Clicking will automatically update the value.
			</p>
		</div>
		<div class="col-md-8">
			<div
				class="btn-group"
				role="group"
				aria-label="Basic checkbox toggle button group"
			>
				<input
					type="checkbox"
					id="isDowntime"
					class="btn-check"
					autocomplete="off"
					v-model="isDowntimeModel"
				/>
				<label
					class="btn btn-outline-primary"
					for="isDowntime"
				>{{ isDowntime() }}</label
				>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "IsDowntime",
	computed: {
		isDowntimeModel: {
			get() {
				return this.$store.state.changeTask.isDowntime;
			},
			set(isDowntime) {
				this.$store.commit({
					type: "updateChangeTaskIsDowntime",
					isDowntime: isDowntime,
				});

				this.updateIsDowntime(isDowntime);
			}
		}
	},
	methods: {
		isDowntime() {
			if (this.isDowntimeModel) {
				return "Downtime Scheduled - click to remove";
			}
			return "No Downtime - click to Schedule";
		},
		updateIsDowntime(isDowntime) {
			this.$store.dispatch("newToast", {
				header: "Updating Downtime flag",
				message: "Please wait, we are updating the downtime flag",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "downtime-save",
			});

			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set('is_downtime', isDowntime);

			//Send to the backend
			this.axios.post(
				"update/is_downtime/",
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Downtime flag",
					message: "Successfully Updated the Downtime Flag",
					extra_classes: "bg-success",
					unique_type: "downtime-save",
				});

			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to Update Downtime Flag",
					message: `We have come across an issue updating the downtime flag. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "downtime-save",
				});

			})
		}
	},
}
</script>