<template>
	<n-config-provider :theme="getTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Requirement Item Information</h1>
				<br/>
				<a
					v-bind:href="`${rootUrl}requirement_information/${requirementItemResults[0].fields.requirement}/`"
				>
					Go Back to requirement
				</a>
				<hr/>

				<div v-if="requirementItemIsClosed"
					 class="alert alert-info"
				>
					Requirement Item is currently closed.
				</div>

				<div class="row">
					<!-- Description -->
					<div class="col-md-4">
						<h2>Description</h2>
						<p class="text-instructions">
							Requirement Items should be detailed. They should only
							focus on one small section of the requirement.
						</p>
					</div>

					<!-- Requirement item information -->
					<div
						class="col-md-8"
						style="min-height: 610px"
					>
						<div class="form-group">
							<label for="requirement_item_title">
								Requirement Item Title:
								<validation-rendering
									v-bind:error-list="v$.requirementItemTitleModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="requirement_item_title"
								class="form-control"
								type="text"
								required="true"
								maxlength="255"
								v-model="requirementItemTitleModel"
								v-bind:disabled="isReadOnly"
							/>
						</div>
						<div class="form-group">
							<label>
								Requirement Item Scope:
								<validation-rendering
									v-bind:error-list="v$.requirementItemScopeModel.$errors"
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
								content_css: `${this.contentCss}`
							}"
								v-model="requirementItemScopeModel"
								v-bind:disabled="isReadOnly"
							/>
						</div>
					</div>
				</div>

				<!-- Stakeholder Information -->
				<hr/>
				<div class="row">
					<!-- Description -->
					<div class="col-md-4">
						<h2>Stakeholder</h2>
					</div>
					<div class="col-md-8 organisation-details">
						<img
							v-bind:src="getStakeholderImage"
							alt="Stakeholder Logo"
							class="organisation-image"
						/>
						<div class="organisation-name">
							{{ stakeholderModel.organisation_name }}
						</div>
						<div class="organisation-link">
							<Icon v-bind:icon="icons.linkOut"></Icon>
							Website:
							<a
								v-bind:href="stakeholderModel.organisation_website"
								target="_blank"
								rel="noopener noreferrer"
							>
								{{ stakeholderModel.organisation_website }}
							</a>
						</div>
						<div class="organisation-email">
							<Icon v-bind:icon="icons.mailIcon"></Icon>
							Email:
							<a
								v-bind:href="`mailto:${stakeholderModel.organisation_email}`"
							>
								{{ stakeholderModel.organisation_email }}
							</a>
						</div>
					</div>
				</div>

				<!-- Status -->
				<hr/>
				<div class="row">
					<div class="col-md-4">
						<h2>Status</h2>
						<p class="text-instructions">
							Set the Requirement Status and Type here.
						</p>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label
							>Requirement Status
								<validation-rendering
									v-bind:error-list="v$.statusOptions.$errors"
								></validation-rendering>
							</label>
							<n-select
								:options="statusOptions"
								label="status"
								v-model:value="statusModel"
								v-bind:disabled="userLevel <= 1"
							></n-select>
						</div>
					</div>
					<div class="col-md-4">
						<div class="form-group">
							<label
							>Requirement Type
								<validation-rendering
									v-bind:error-list="v$.typeModel.$errors"
								></validation-rendering>
							</label>
							<n-select
								:options="typeOptions"
								label="type"
								v-model:value="typeModel"
								v-bind:disabled="isReadOnly"
							></n-select>
						</div>
					</div>
				</div>

				<!-- Submit Button -->
				<hr v-if="!isReadOnly"/>
				<div
					v-if="!isReadOnly"
					class="row submit-row"
				>
					<div class="col-md-12">
						<button class="btn btn-primary"
								v-on:click="updateRequirementItem"
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
import {Icon} from "@iconify/vue";
import Editor from "@tinymce/tinymce-vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

//Mixins
import getThemeMixin from "../../mixins/getThemeMixin";
import iconMixin from "../../mixins/iconMixin";
import uploadMixin from "../../mixins/uploadMixin";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";
import {isReadOnly} from "vuedraggable/src/core/sortableEvents";

export default {
	name: "RequirementItemInformation.vue",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		Icon,
		NSelect,
		ValidationRendering,
	},
	props: {
		requirementItemResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		organisationResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		defaultStakeholderImage: {
			type: String,
			default: "/",
		},
		requirementItemIsClosed: {
			type: Boolean,
			default: false,
		},
		statusOptions: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: ""
		},
		typeOptions: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userLevel: {
			type: Number,
			default: 0,
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			rootUrl: "getRootUrl",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
		}),
		getStakeholderImage() {
			const image =
				this.stakeholderModel.organisation_profile_picture;
			if (image === "" || image === null) {
				//There is no image - return the default image
				return this.defaultStakeholderImage;
			}
			return `${this.rootUrl}private/${this.stakeholderModel.organisation_profile_picture}`;
		},
	},
	mixins: [getThemeMixin, iconMixin, uploadMixin],
	data() {
		return {
			isReadOnly: false,
			requirementItemScopeModel: this.requirementItemResults[0].fields.requirement_item_scope,
			requirementItemTitleModel: this.requirementItemResults[0].fields.requirement_item_title,
			stakeholderModel: this.organisationResults[0].fields,

			statusModel: this.requirementItemResults[0].fields.requirement_item_status,
			typeModel: this.requirementItemResults[0].fields.requirement_item_type,
		};
	},
	watch: {
		async statusModel() {
			//Escape condition 1 - if the project is NOT already closed
			if (!this.requirementItemIsClosed) return;

			//Escape condition 2 - if the NEW status is closed
			if (this.checkStatusIsClosed()) return;

			//Method - we want to resave the data and then reload
			await this.updateRequirementItem();
			window.location.reload();
		},
	},
	validations: {
		requirementItemScopeModel: {
			required,
			maxLength: maxLength(630000),
		},
		requirementItemTitleModel: {
			required,
		},
		statusOptions: {
			required,
		},
		statusModel: {
			required,
		},
		typeModel: {
			required,
		},
	},
	methods: {
		checkStatusIsClosed() {
			//Will filter the current status for the status - then check to see if it is closed
			const filtered_status = this.statusOptions.filter((row) => {
				return parseInt(row.value) === parseInt(this.statusModel);
			});

			//If there are not matching status - return true. Assume closed
			if (filtered_status.length === 0) return true;

			//Use the first value
			return filtered_status[0].requirement_item_higher_order_status === "Closed";
		},
		setReadOnly() {
			//If the prop has been set as read only
			if (this.requirementItemIsClosed) {
				this.isReadOnly = true;
				return;
			}

			//If the requirement item status is closed => set the isReadOnly to true
			if (this.checkStatusIsClosed()) {
				this.isReadOnly = true;
				return;
			}

			//If the user level is 1 or below
			if (this.userLevel <= 1) {
				this.isReadOnly = true;
			}
		},
		updateRequirementItem() {
			// Check the validation first
			this.v$.$touch();

			if (this.v$.$invalid) {
				//Notify the user of the issues
				this.$store.dispatch("newToast", {
					header: "Error Saving",
					message: "Please fill out the form appropriately",
					extra_classes: "bg-warning text-dark",
					delay: 0,
					unique_type: "saving",
				});

				//Just return - as we do not need to do the rest of this function
				return;
			}

			//Open up the loading modal
			this.$store.dispatch("newToast", {
				header: "Saving Requirement Item",
				message: "We are saving your requirement item. Please wait",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "saving",
			});

			// Set up the data object to send
			const data_to_send = new FormData();
			data_to_send.set(
				"requirement_item_title",
				this.requirementItemTitleModel
			);
			data_to_send.set(
				"requirement_item_scope",
				this.requirementItemScopeModel
			);
			data_to_send.set("requirement_item_status", this.statusModel);
			data_to_send.set("requirement_item_type", this.typeModel);

			// Use Axion to send the data
			this.axios.post(
				"save/",
				data_to_send
			).then((response) => {
				//Tell user of successfull update
				this.$store.dispatch("newToast", {
					header: "Saved Requirement Item",
					message: "Your Requirement Item has saved",
					extra_classes: "bg-success",
					unique_type: "saving",
				});

				//Reload the page IF the status is closed
				if (this.checkStatusIsClosed()) {
					window.location.reload();
				}
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Saving Requirement Item",
					message: `Sorry, your requirement item failed to save. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
					unique_type: "saving",
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
