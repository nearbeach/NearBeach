<template>
	<div
		class="modal fade"
		id="newItemModal"
		tabindex="-1"
		aria-labelledby="requirementItemModal"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-xl modal-fullscreen-lg-down">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.clipboardIcon"></Icon>
						New
						Requirement Item Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="requirementItemCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Description</strong>
							<p class="text-instructions">
								Place in a detailed description of this
								requirement item. This particular item can be
								then connected to Project or Tasks.
							</p>
						</div>
						<div class="col-md-8">
							<label for="id_requirement_item_title"
							>Requirement Item Title:
								<validation-rendering
									v-bind:error-list="v$.requirementItemTitleModel.$errors"
								></validation-rendering>
							</label>
							<input
								id="id_requirement_item_title"
								class="form-control"
								name="requirement_item_title"
								type="text"
								required="true"
								maxlength="255"
								v-model="requirementItemTitleModel"
							/>

							<br/>
							<label>
								Requirement Item Scope:
								<validation-rendering
									v-bind:error-list="v$.requirementItemTitleModel.$errors"
								></validation-rendering>
							</label>
							<br/>
							<editor
								:init="{
									height: 500,
									menubar: false,
									plugins: ['lists', 'codesample', 'table'],
            						toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
											 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            						skin: `${this.skin}`,
						            content_css: `${this.contentCss}`
								}"
								v-model="requirementItemScopeModel"
							/>
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
										v-bind:error-list="v$.requirementItemTitleModel.$errors"
									></validation-rendering>
								</label>
								<n-select
									:options="statusItemFixList"
									label="status"
									v-model:value="statusItemModel"
								></n-select>
							</div>
						</div>
						<div class="col-md-4">
							<div class="form-group">
								<label
								>Requirement Type
									<validation-rendering
										v-bind:error-list="v$.typeItemModel.$errors"
									></validation-rendering>
								</label>
								<n-select
									:options="typeItemFixList"
									label="type"
									v-model:value="typeItemModel"
								></n-select>
							</div>
						</div>
					</div>
				</div>

				<!-- FOOTERS -->
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="saveItem"
					>
						Save Requirement Item
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";
import Editor from "@tinymce/tinymce-vue";

//Mixins
import iconMixin from "../../../mixins/iconMixin";

//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../../validation/ValidationRendering.vue";

//Vuex
import {mapGetters} from "vuex";

export default {
	name: "NewRequirementItemWizard",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		Icon,
		NSelect,
		ValidationRendering,
	},
	mixins: [iconMixin],
	data() {
		return {
			requirementItemScopeModel: "",
			requirementItemTitleModel: "",
			statusItemFixList: [],
			statusItemModel: "",
			typeItemFixList: [],
			typeItemModel: "",
		};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			skin: "getSkin",
		}),
	},
	validations: {
		requirementItemScopeModel: {
			required,
			maxLength: maxLength(630000),
		},
		requirementItemTitleModel: {
			required,
		},
		statusItemModel: {
			required,
		},
		typeItemModel: {
			required,
		},
	},
	methods: {
		saveItem() {
			// Check the validation first
			this.v$.$touch();

			if (this.v$.$invalid) {
				//Just return - as we do not need to do the rest of this function
				return;
			}

			const data_to_send = new FormData();
			data_to_send.set(
				"requirement_item_title",
				this.requirementItemTitleModel
			);
			data_to_send.set(
				"requirement_item_scope",
				this.requirementItemScopeModel
			);
			data_to_send.set(
				"requirement_item_status",
				this.statusItemModel
			);
			data_to_send.set("requirement_item_type", this.typeItemModel);

			this.axios.post(
				`${this.rootUrl}new_requirement_item/save/${this.locationId}/`,
				data_to_send
			).then((response) => {
				//Data saved successfully - clear all models
				this.requirementItemScopeModel = "";
				this.requirementItemTitleModel = "";
				this.statusItemModel = "";
				this.typeItemModel = "";

				//EMIT THE NEW DATA UPSTREAM
				this.$emit("new_item_added", response.data);

				//SHOULD CLOSE MODAL HERE!
				document
					.getElementById("requirementItemCloseButton")
					.click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to save item",
					message: `Failed to save item. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateStatusList() {
			this.axios.post(
				`${this.rootUrl}requirement_information/data/list_of_item_status_values/`
			).then((response) => {
				this.statusItemFixList = response.data.map((row) => {
					return {
						value: row.pk,
						label: row.fields.requirement_item_status,
					}
				})
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Status List",
					message: `There was an error updating the status list - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		updateTypeList() {
			this.axios.post(
				`${this.rootUrl}requirement_information/data/list_of_item_type_values/`
			).then((response) => {
				this.typeItemFixList = response.data.map((row) => {
					return {
						value: row.pk,
						label: row.fields.requirement_item_type,
					}
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error Updating Type List",
					message: `There was an error updating the type list - error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		this.$nextTick(() => {
			this.updateStatusList();
			this.updateTypeList();
		})
	}
};
</script>

<style scoped></style>
