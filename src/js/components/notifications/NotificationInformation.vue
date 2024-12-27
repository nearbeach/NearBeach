<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Notification Information</h1>
				<br/>
				<a v-bind:href="`${rootUrl}search/notification/`">Go back to Notification Search</a>
				<hr/>

				<div class="row">
					<!-- DESCRIPTION -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Notifications will only show between their start and end date. So you
							can prepare notifications for a release in the future.
						</p>
					</div>

					<!-- NOTIFICATION FORM -->
					<div class="col-md-8">
						<div class="form-group">
							<label>
								Notification Name
								<validation-rendering
									v-bind:error-list="v$.headerModel.$errors"
								></validation-rendering>
							</label>
							<input type="text"
								   v-model="headerModel"
								   class="form-control"
							/>
						</div>
						<br/>
						<div class="form-group">
							<label>
								Notification Message
								<validation-rendering
									v-bind:error-list="v$.messageModel.$errors"
								></validation-rendering>
							</label>
							<textarea v-model="messageModel"
									  class="form-control"
							></textarea>
						</div>
					</div>
				</div>

				<hr/>
				<between-dates
					destination="notification"
					v-on:update_dates="updateDates($event)"
				></between-dates>

				<div class="row">
					<div class="col-md-4">
						<h2>Notification Location</h2>
						<p class="text-instructions">
							The notifications can show on either or both the login screen, or dashboard.
						</p>
					</div>
					<div class="col-md-8">
						<n-select :options="locationList"
								  v-model:value="locationModel"
						></n-select>
					</div>
				</div>

				<!-- Submit Button -->
				<hr/>
				<div class="row submit-row">
					<div class="col-md-12">
						<button class="btn btn-warning"
								v-on:click="deleteNotification"
						>
							Delete Notification
						</button>
						<button class="btn btn-primary save-changes"
								v-on:click="updateNotification"
						>
							Update Notification
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import BetweenDates from "../dates/BetweenDates.vue";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//Naive ui
import { NSelect } from "naive-ui";

//Composables
import {useNBTheme} from "../../composables/theme/useNBTheme";


export default {
	name: "NewNotification",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		BetweenDates,
		NSelect,
		ValidationRendering,
	},
	props: {
		notificationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			endDateModel: this.notificationResults[0].fields.notification_end_date,
			headerModel: this.notificationResults[0].fields.notification_header,
			locationList: [
				{value: "all", label: "All Options"},
				{value: "dashboard", label: "Dashboard Screen"},
				{value: "login", label: "Login Screen"},
			],
			locationModel: this.notificationResults[0].fields.notification_location,
			messageModel: this.notificationResults[0].fields.notification_message,
			startDateModel: this.notificationResults[0].fields.notification_start_date,
		};
	},
	validations: {
		endDateModel: {
			required,
		},
		headerModel: {
			required,
			maxLength: maxLength(255),
		},
		messageModel: {
			required,
			maxLength: maxLength(630000),
		},
		startDateModel: {
			required,
		},
	},
	methods: {
		useNBTheme,
		deleteNotification() {
			const data_to_send = new FormData();
			data_to_send.set("notification_id", this.notificationResults[0].pk);

			this.axios.post(
				`${this.rootUrl}notification_information/delete/`,
				data_to_send,
			).then(() => {
				//Go back to search
				window.location.href = `${this.rootUrl}search/notification/`;
			}).catch(() => {
				this.$store.dispatch("newToast", {
					header: "Can not delete",
					message: "Sorry, we are having issues deleting this notification. Please contact your system admin",
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateDates(data) {
			//Update both the start and end dates
			this.startDateModel = new Date(data.start_date);
			this.endDateModel = new Date(data.end_date);
		},
		async updateNotification() {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect) {
				return;
			}

			//Create data_to_send
			const data_to_send = new FormData();
			data_to_send.set('notification_header', this.headerModel);
			data_to_send.set('notification_message', this.messageModel);
			data_to_send.set('notification_location', this.locationModel);
			data_to_send.set(
				'notification_start_date',
				this.startDateModel.toISOString()
			);
			data_to_send.set(
				'notification_end_date',
				this.endDateModel.toISOString(),
			);

			this.axios.post(
				`${this.rootUrl}notification_information/${this.notificationResults[0].pk}/save/`,
				data_to_send,
			).then(() => {
				//Tell user that this was successful
				this.$store.dispatch("newToast", {
					header: "Saved Notification",
					message: "Your notification has saved.",
					extra_classes: "bg-success",
					unique_type: "save",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not save Notification",
					message: `Error saving notification. Error: ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		//Update user level
		this.$store.commit({
			type: "updateUserLevel",
			userLevel: 4,
		});
	},
}

</script>
