<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body requirement-border">
				<h1>Requirement Information</h1>
				<hr/>

				<div
v-if="requirementIsClosed"
					 class="alert alert-info"
				>
					Requirement is currently closed.
				</div>

				<div class="row">
					<!-- Description -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Place a basic bird's eye view of the requirement
							description here. You will be able to break the
							requirement down into smaller components called 'Items'
							below in the 'Requirement Item' section.
						</p>
					</div>

					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<div class="form-group">
							<label for="id_requirement_title"
							>Requirement Title:
								<validation-rendering
									:error-list="v$.requirementTitleModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="id_requirement_title"
								v-model="requirementTitleModel"
								class="form-control"
								name="requirement_title"
								type="text"
								required="true"
								maxlength="255"
								:disabled="isReadOnly"
							/>
						</div>

						<br/>
						<label>
							Requirement Scope:
							<validation-rendering
								:error-list="v$.requirementScopeModel.$errors"
							></validation-rendering>
						</label>
						<br/>
						<img
							:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
							class="loader-image"
							alt="loading image for Tinymce"
						/>
						<editor
							v-model="requirementScopeModel"
							license-key="gpl"
							:init="{
							license_key: 'gpl',
							file_picker_types: 'image',
							height: 500,
							images_upload_handler: useUploadImage,
							menubar: false,
							paste_data_images: true,
							plugins: ['lists', 'image', 'codesample', 'table'],
            				toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
									 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
							skin: `${skin}`,
							content_css: `${contentCss}`,
							relative_urls: false,
						}"
							:disabled="isReadOnly"
						/>
					</div>
				</div>

				<!-- Stakeholder Information -->
				<hr/>
				<stakeholder-information
					:organisation-results="organisationResults"
					:default-stakeholder-image="defaultStakeholderImage"
				></stakeholder-information>

				<!-- Status -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<h2>Status</h2>
						<p class="text-instructions">
							Set the Requirement Status and Type here.
						</p>
					</div>
					<div class="col-md-8">
						<div class="row">
							<div class="col-md-6">
								<div class="form-group">
									<label
									>Requirement Status
										<validation-rendering
											:error-list="v$.statusModel.$errors"
										></validation-rendering>
									</label>
									<n-select
										v-model:value="statusModel"
										:options="statusOptions"
										:disabled="userLevel <= 1"
										:clearable="false"
										label="status"
									></n-select>
								</div>
							</div>
							<div class="col-md-6">
								<div class="form-group">
									<label
									>Requirement Type
										<validation-rendering
											:error-list="v$.typeModel.$errors"
										></validation-rendering>
									</label>
									<n-select
										v-model:value="typeModel"
										:options="typeList"
										:disabled="isReadOnly"
										:clearable="false"
										label="type"
									></n-select>
								</div>
							</div>
						</div>
					</div>
				</div>

				<!-- Submit Button -->
				<hr v-if="!isReadOnly" />
				<div
					v-if="!isReadOnly"
					class="row submit-row"
				>
					<div class="col-md-12">
						<button
class="btn btn-primary save-changes"
								@click="updateRequirement"
						>
							Update Requirement
						</button>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//JavaScript Libraries
import Editor from "@tinymce/tinymce-vue";
import {NSelect} from "naive-ui";
import StakeholderInformation from "Components/organisations/StakeholderInformation.vue";

//VueX
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "Components/validation/ValidationRendering.vue";

//Composables
import {useNBTheme} from "Composables/theme/useNBTheme";
import {useUploadImage} from "Composables/uploads/useUploadImage";

export default {
	name: "RequirementInformation",
	components: {
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
			default() {
				return [];
			},
		},
		requirementIsClosed: {
			type: Boolean,
			default: false,
		},
		requirementResults: {
			type: Array,
			default() {
				return [];
			},
		},
		statusOptions: {
			type: Array,
			default() {
				return [];
			},
		},
		theme: {
			type: String,
			default: "",
		},
		typeList: {
			type: Array,
			default() {
				return [];
			},
		},
		userLevel: {
			type: Number,
			default: 0
		},
	},
	setup() {
		return {v$: useVuelidate()};
	},
	data() {
		return {
			isReadOnly: false,
			requirementScopeModel: this.requirementResults[0].fields.requirement_scope,
			requirementTitleModel: this.requirementResults[0].fields.requirement_title,
			stakeholderModel: "",
			statusModel: this.requirementResults[0].fields.requirement_status,
			typeModel: this.requirementResults[0].fields.requirement_type,
		};
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
		async statusModel() {
			//Escape condition 1 - if the project is NOT already closed
			if (!this.requirementIsClosed) return;

			//Escape condition 2 - if the NEW status is closed
			if (this.checkStatusIsClosed()) return;

			//Method - we want to resave the data and then reload
			await this.updateRequirement();
			window.location.reload();
		},
	},
	validations: {
		requirementScopeModel: {
			required,
			maxLength: maxLength(630000),
		},
		requirementTitleModel: {
			required,
		},
		statusModel: {
			required,
		},
		typeModel: {
			required,
		},
	},
	async beforeMount() {
		await this.$store.dispatch("processThemeUpdate", {
			theme: this.theme,
		});
	},
	mounted() {
		//Check for the read only
		this.setReadOnly();

		this.$store.commit({
			type: "updateTitle",
			title: this.requirementTitleModel,
		});
	},
	methods: {
		useUploadImage,
		useNBTheme,
		checkStatusIsClosed() {
			//Will filter the current status for the status - then check to see if it is closed
			const filtered_status = this.statusOptions.filter((row) => {
				return parseInt(row.value) === parseInt(this.statusModel);
			});

			//If there are not matching status - return true. Assume closed
			if (filtered_status.length === 0) return true;

			//Use the first value
			return filtered_status[0].requirement_higher_order_status === "Closed";
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
		updateRequirement() {
			// Check the validation first
			this.v$.$touch();

			if (this.v$.$invalid) {
				this.$store.dispatch("newToast", {
					header: "Please check validation",
					message: "Sorry, but can you please fix all validation issues.",
					extra_classes: "bg-warning text-dark",
					delay: 0,
				});

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Notify user of attempting to save
			this.$store.dispatch("newToast", {
				header: "Requirement Currently Saving",
				message: "Please wait whilst we save the requirement",
				extra_classes: "bg-warning text-dark",
				unique_type: "save",
				delay: 0,
			});

			// Set up the data object to send
			const data_to_send = new FormData();
			data_to_send.set(
				"requirement_title",
				this.requirementTitleModel
			);
			data_to_send.set(
				"requirement_scope",
				this.requirementScopeModel
			);
			data_to_send.set("requirement_status", this.statusModel);
			data_to_send.set("requirement_type", this.typeModel);

			// Use Axion to send the data
			this.axios.post(
				"save/",
				data_to_send
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Requirement was save",
					message: "Requirement saved successfully",
					extra_classes: "bg-success",
					unique_type: "save",
					delay: 0,
				});

				//If the status is closed - refresh the page
				if (this.checkStatusIsClosed()) {
					window.location.reload();
				}
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Requirement Could not save",
					message: `There was an error saving the requirement. Error -> ${error}`,
					extra_classes: "bg-danger",
					unique_type: "save",
					delay: 0,
				});
			});
		},
	},
};
</script>


