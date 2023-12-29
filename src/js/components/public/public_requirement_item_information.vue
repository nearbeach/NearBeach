<template>
	<div class="modal fade"
		 id="item_modal"
		 tabindex="-1"
		 role="dialog"
		 aria-hidden="true"
	>
		<div class="modal-dialog modal-xl">
			<div class="modal-content">
				<div class="modal-header">
					<h2>Requirement Item Information</h2>
					<button type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
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
								</label>
								<input
									id="requirement_item_title"
									v-model="requirementItemTitleModel"
									class="form-control"
									type="text"
									disabled
								/>
							</div>
							<div class="form-group">
								<label>
									Requirement Item Scope:
								</label>
								<br/>
								<img
									v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
									class="loader-image"
									alt="loading image for Tinymce"
								/>
								<editor
									:init="{
									height: 500,
									menubar: false,
									plugins: ['lists', 'image', 'codesample', 'table'],
            						toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
											 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
									skin: `${this.skin}`,
									content_css: `${this.contentCss}`,
								}"
									v-model="requirementItemScopeModel"
									v-bind:disabled="true"
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
								<label>Requirement Status</label>
								<n-select
									:options="statusFixList"
									label="status"
									v-model:value="statusModel"
									disabled
								></n-select>
							</div>
						</div>
						<div class="col-md-4">
							<div class="form-group">
								<label>Requirement Type</label>
								<n-select
									:options="typeFixList"
									label="type"
									v-model:value="typeModel"
									disabled
								></n-select>
							</div>
						</div>
					</div>

				</div>
				<div class="modal-footer">
					<button type="button"
							class="btn btn-secondary"
							data-bs-dismiss="modal"
					>
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {Icon} from "@iconify/vue";
import editor from "@tinymce/tinymce-vue";
import ValidationRendering from "../validation/ValidationRendering.vue";
import { NSelect } from "naive-ui";

//VueX
import { mapGetters } from "vuex";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "PublicRequirementItemInformation",
	components: {
		editor,
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
		statusList: {
			type: Array,
			default: () => {
				return [];
			},
		},
		theme: {
			type: String,
			default: ""
		},
		typeList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	mixins: [iconMixin],
	data() {
		return {
			requirementItemScopeModel: "",
			requirementItemTitleModel: "",
			stakeholderModel: "",

			statusFixList: [],
			statusModel: "",
			typeFixList: [],
			typeModel: "",
		};
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
	watch: {
		requirementItemResults(new_results) {
			// If the requirement item results has length 0, do nothing
			if (this.requirementItemResults.length === 0) return;

			//Update the variables
			this.requirementItemScopeModel = new_results[0].fields.requirement_item_scope;
			this.requirementItemTitleModel = new_results[0].fields.requirement_item_title;
			this.stakeholderModel = this.organisationResults[0].fields;
			this.statusModel = new_results[0].fields.requirement_item_status;
			this.typeModel = new_results[0].fields.requirement_item_type;
		},
	},
	mounted() {
		//Map the original lists to something NSelect can read
		this.statusFixList = this.statusList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_item_status,
			};
		});

		this.typeFixList = this.typeList.map((row) => {
			return {
				value: row.pk,
				label: row.fields.requirement_item_type,
			};
		});
	},
}
</script>