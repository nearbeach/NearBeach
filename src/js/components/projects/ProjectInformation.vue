<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Project Information</h1>
				<hr/>

				<div v-if="projectIsClosed"
					 class="alert alert-info"
				>
					Project is currently closed
				</div>

				<div class="row">
					<!-- DESCRIPTION -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Edit the project information and then click the "Update
							Project" button at the bottom of the page
						</p>
					</div>

					<!-- PROJECT FORM -->
					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<!-- PROJECT NAME -->
						<div class="form-group">
							<label
							>Project Name
								<validation-rendering
									v-bind:error-list="v$.projectNameModel.$errors"
								></validation-rendering>
							</label>
							<input
								type="text"
								v-model="projectNameModel"
								class="form-control"
								v-bind:disabled="isReadOnly"
							/>
						</div>
						<br/>

						<!-- PROJECT DESCRIPTION -->
						<label>
							Project Description:
							<validation-rendering
								v-bind:error-list="v$.projectDescriptionModel.$errors"
							></validation-rendering>
						</label>
						<br/>
						<img
							v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
							class="loader-image"
							alt="loading image for Tinymce"
						/>
						<editor
							:init="{
							file_picker_types: 'image',
							height: 500,
							images_upload_handler: uploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 				 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${this.skin}`,
							content_css: `${this.contentCss}`,
						}"
							v-bind:disabled="isReadOnly"
							v-model="projectDescriptionModel"
						/>
					</div>
				</div>

				<!-- PROJECT STATUS -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<strong>Project Status</strong>
						<p class="text-instructions">
							Please update the project's task to reflect it's current
							status. Then click on the "Update Project" button to
							save the change.
						</p>
					</div>
					<div class="col-md-4">
						<n-select
							v-bind:options="statusOptions"
							v-bind:disabled="userLevel<=1"
							v-model:value="projectStatusModel"
						></n-select>
					</div>
				</div>

				<!-- STAKEHOLDER ORGANISATION -->
				<hr/>
				<stakeholder-information
					v-bind:organisation-results="organisationResults"
					v-bind:default-stakeholder-image="defaultStakeholderImage"
				></stakeholder-information>

				<!-- START DATE & END DATE -->
				<hr/>
				<between-dates
					destination="project"
					v-on:update_dates="updateDates($event)"
					v-bind:is-read-only="isReadOnly"
					v-bind:end-date-model="projectEndDateModel.getTime()"
					v-bind:start-date-model="projectStartDateModel.getTime()"
				></between-dates>

				<!-- Submit and Close Button -->
				<hr v-if="!isReadOnly"/>
				<div
					class="row submit-row"
					v-if="!isReadOnly"
				>
					<div class="col-md-12">
						<!-- Update Project -->
						<button class="btn btn-primary save-changes"
							v-on:click="updateProject"
						>
							Update Project
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NSelect} from "naive-ui";
import BetweenDates from "../dates/BetweenDates.vue";
import StakeholderInformation from "../organisations/StakeholderInformation.vue";
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";

//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import uploadMixin from "../../mixins/uploadMixin";

export default {
	name: "ProjectInformation",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		BetweenDates,
		editor: Editor,
		NSelect,
		StakeholderInformation,
		ValidationRendering,
	},
	props: {
		defaultStakeholderImage: {
			type: String,
			default: "",
		},
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		projectIsClosed: {
			type: Boolean,
			default: false,
		},
		projectResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		statusOptions: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: "",
		},
		userLevel: {
			type: Number,
			default: 1,
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
		}),
	},
	watch: {
		async projectStatusModel() {
			//Escape condition 1 - if the project is NOT already closed
			if (!this.projectIsClosed) return;

			//Escape condition 2 - if the NEW status is closed
			if (this.checkStatusIsClosed()) return;

			//Method - we want to resave the data and then reload
			await this.updateProject();
			window.location.reload();
		},
	},
	mixins: [getThemeMixin, uploadMixin],
	data() {
		return {
			isReadOnly: false,
			projectDescriptionModel: this.projectResults[0].fields.project_description,
			projectEndDateModel: new Date(
				this.projectResults[0].fields.project_end_date
			),
			projectNameModel: this.projectResults[0].fields.project_name,
			projectStartDateModel: new Date(
				this.projectResults[0].fields.project_start_date
			),
			projectStatusModel: this.projectResults[0].fields.project_status,
		};
	},
	validations: {
		projectDescriptionModel: {
			required,
			maxLength: maxLength(630000),
		},
		projectEndDateModel: {
			required,
		},
		projectNameModel: {
			maxLength: maxLength(255),
			required,
		},
		projectStartDateModel: {
			required,
		},
	},
	methods: {
		checkStatusIsClosed() {
			//Will filter the current status for the status - then check to see if it is closed
			const filtered_status = this.statusOptions.filter((row) => {
				return parseInt(row.value) === parseInt(this.projectStatusModel);
			});

			//If there are not matching status - return true. Assume closed
			if (filtered_status.length === 0) return true;

			//Use the first value
			return filtered_status[0].project_higher_order_status === "Closed";
		},
		setReadOnly() {
			//If the project status is closed => set the isReadOnly to true
			if (this.checkStatusIsClosed()) {
				this.isReadOnly = true;
				return;
			}

			//If the user level is 1 or below
			if (this.userLevel <= 1) {
				this.isReadOnly = true;
			}
		},
		updateDates(data) {
			this.projectEndDateModel = new Date(data.end_date);
			this.projectStartDateModel = new Date(data.start_date);
		},
		async updateProject() {
			//Check validation
			const isFormCorrect = await this.v$.$validate();
			if (!isFormCorrect) {
				return;
			}

			//Construct data_to_send to backend
			const data_to_send = new FormData();
			data_to_send.set(
				"project_description",
				this.projectDescriptionModel
			);
			data_to_send.set(
				"project_end_date",
				this.projectEndDateModel.toISOString()
			);
			data_to_send.set("project_name", this.projectNameModel);
			data_to_send.set(
				"project_start_date",
				this.projectStartDateModel.toISOString()
			);
			data_to_send.set("project_status", this.projectStatusModel);

			//Notify user of attempting to save
			this.$store.dispatch("newToast", {
				header: "Project Currently Saving",
				message: "Please wait whilst we save the project",
				extra_classes: "bg-warning text-dark",
				unique_type: "save",
				delay: 0,
			});

			//Use axios to send data
			this.axios
				.post(
					`${this.rootUrl}project_information/${this.projectResults[0].pk}/save/`,
					data_to_send
				)
				.then(() => {
					//Notify user of success update
					this.$store.dispatch("newToast", {
						header: "Project Saved",
						message: "Project Saved",
						extra_classes: "bg-success",
						unique_type: "save",
					});

					//Reload the page IF the status is closed
					if (this.checkStatusIsClosed()) {
						window.location.reload();
					}
				})
				.catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Project Could not save",
						message: `There was an error saving the project. Error -> ${error}`,
						extra_classes: "bg-danger",
						unique_type: "save",
						delay: 0,
					});
				});
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Set the read only status
		this.setReadOnly();
	},
};
</script>

<style scoped></style>
