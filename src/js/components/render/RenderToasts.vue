<template>
	<div class="toast-container">
		<div v-for="(single_toast, index) in toastList"
			 :key="index"
			 v-bind:class="`toast ${single_toast.extra_classes}`"
			 role="alert"
			 aria-live="assertive"
			 aria-atomic="true"
			 v-bind:data-delay="single_toast.delay"
		>
			<div class="toast-header">
				<strong class="me-auto">{{ single_toast.header }}</strong>
				<small>{{ getTime(single_toast.timestamp) }}</small>
				<button type="button"
						class="btn-close"
						aria-label="Close"
						v-on:click="removeToast(single_toast.unique_uuid)"
				></button>
			</div>
			<div class="toast-body">
				{{ single_toast.message }}
			</div>
		</div>
	</div>
</template>

<script>
import { mapGetters } from "vuex";
import { Toast } from "bootstrap";

export default {
	name: "RenderToasts",
	props: {},
	computed: {
		...mapGetters({
			toastList: "getToastList",
		})
	},
	watch: {
		toastList() {
			//Wait until AFTER rendering happens
			this.$nextTick(() => {
				// let toastList = document.getElementsByClassName("toast");
				const toastList = [].slice.call(document.querySelectorAll('.toast'))

				//Loop through each toast item and deploy :)
				toastList.forEach((row) => {
					//Get the delay
					const delay = row.dataset.delay;

					//Setup the options
					const options = {
						delay: parseInt(delay),
						autohide: parseInt(delay) > 0,
					};

					//Create the new toast
					const toast = new Toast(row, options);

					//Show the toast
					toast.show();
				})
			})
		},
	},
	methods: {
		getTime(raw_timestamp) {
			//Get the date object
			const timestamp = new Date(raw_timestamp);

			//Get the hours
			let hours = timestamp.getHours();

			//Determine if hours are AM or PM
			const ampm = hours >= 12 ? 'PM' : 'AM';

			//Reset hours into non 24 format
			hours = hours % 12;
			hours = hours ? hours : 12;

			//Get minutes in the 00 format
			const minutes = timestamp.getMinutes() < 10 ? `0${timestamp.getMinutes()}` : timestamp.getMinutes();

			//Return what we have
			return `${hours}:${minutes} ${ampm}`;
		},
		removeToast(unique_uuid) {
			this.$store.dispatch("removeToast", {
				unique_uuid,
			});
		}
	},
}
</script>