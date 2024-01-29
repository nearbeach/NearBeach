<template xmlns:v-bind="http://www.w3.org/1999/xhtml">
	<div class="card">
		<div class="card-body">
			<h1>Search Notifications</h1>
			<hr/>

			<!-- SEARCH FIELD-->
			<div class="form-row">
				<div class="form-group">
					<label>Search:</label>
					<input
						type="text"
						class="form-control search-organisation"
						v-model="searchModel"
						maxlength="250"
					/>
				</div>
			</div>
			<hr/>

			<!-- Search Results -->
			<div class="list-group"
				 v-if="localNotificationResults.length > 0"
			>
				<a
					class="list-group-item list-group-item-action"
					v-for="notification in localNotificationResults"
					:key="notification.pk"
					v-bind:href="`/notification_information/${notification.pk}/`"
				>
					<strong>{{ notification.fields.notification_header }}</strong>
					<br/>
					<p class="small-text">
						{{ notification.fields.notification_message }}
					</p>
				</a>
			</div>

			<div class="alert alert-warning"
				 v-else
			>
				Sorry, there are no notifications
			</div>

			<hr/>
			<div class="row submit-row">
				<div class="col-md-12">
					<a
						v-bind:href="`${rootUrl}new_notification/`"
						class="btn btn-primary save-changes"
					>
						Add new Notification
					</a>
				</div>
			</div>
		</div>
	</div>

</template>

<script>

export default {
	name: "SearchNotifications",
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
	},
	data() {
		return {
			localNotificationResults: this.notificationResults,
			searchModel: "",
			searchTimeout: "",
		}
	},
	methods: {
		getSearchResults() {
			//Setup data_to_send
			const data_to_send = new FormData();
			data_to_send.set("search", this.searchModel);

			//Use Axios to send data
			this.axios.post(
				`${this.rootUrl}search/notification/data/`,
				data_to_send,
			).then((response) => {
				this.localNotificationResults = response.data;
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error getting search results",
					message: `Sorry, we could not retrieve the search results. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		}
	},
	watch: {
		searchModel() {
			//Clear timer if it already exists
			if (this.searchTimeout !== "") {
				//Stop the clock
				clearTimeout(this.searchTimeout);
			}

			//Setup timer if there are 3 characters or more
			if (this.searchModel.length >= 3) {
				//Start the potential search
				this.searchTimeout = setTimeout(() => {
					this.getSearchResults();
				}, 500);
			}
		},
	}
}
</script>