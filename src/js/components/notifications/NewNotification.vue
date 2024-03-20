<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>New Notification</h1>
				<hr/>

				<div class="row">
					<!-- DESCRIPTION -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							To create a new notification, fill out the form and submit it at the
							bottom of the page.
						</p>
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
						<button class="btn btn-primary save-changes"
								v-on:click="submitNewNotification"
						>
							Create new Notification
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import BetweenDates from "../dates/BetweenDates.vue";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//Naive ui
import { NSelect } from "naive-ui";


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
		rootUrl: {
			type: String,
			default: "/",
		},
		staticUrl: {
			type: String,
			default: "/",
		},
		theme: {
			type: String,
			default: "",
		},
	},
	mixins: [getThemeMixin],
	data() {
		return {
			endDateModel: "",
			headerModel: "",
			locationList: [
				{value: "all", label: "All Options"},
				{value: "dashboard", label: "Dashboard Screen"},
				{value: "login", label: "Login Screen"},
			],
			locationModel: "all",
			messageModel: "",
			startDateModel: "",
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
		submitNewNotification: async function() {
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
				`${this.rootUrl}new_notification_save/`,
				data_to_send,
			).then((response) => {
				//Go to the new notification
				window.location.href = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error submitting new notifications",
					message: `Sorry, we could not submit the new notification. Error -> ${error}`,
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