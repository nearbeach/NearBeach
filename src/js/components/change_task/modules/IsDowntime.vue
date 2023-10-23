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
import axios from "axios";

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
			//Setup data to send
			const data_to_send = new FormData();
			data_to_send.set('is_downtime', isDowntime);

			//Send to the backend
			axios.post(
				"update/is_downtime/",
				data_to_send,
			).then((response) => {
				//ADD CODE
			}).catch((error) => {
			})
		}
	},
}
</script>