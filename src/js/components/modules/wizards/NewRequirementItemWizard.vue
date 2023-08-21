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
						<Icon v-bind:icon="icons.clipboardIcon"></Icon> New
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

							<br />
							<label>
								Requirement Item Scope:
								<validation-rendering
									v-bind:error-list="v$.requirementItemTitleModel.$errors"
								></validation-rendering>
							</label>
							<br />
							<editor
								:init="{
									height: 500,
									menubar: false,
									plugins: ['lists', 'codesample', 'table'],
									toolbar: [
										'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
										'bold italic strikethrough underline backcolor | table | ' +
											'bullist numlist outdent indent | removeformat | codesample',
									],
								}"
								v-bind:content_css="false"
								v-bind:skin="false"
								v-model="requirementItemScopeModel"
							/>
						</div>
					</div>

					<!-- Status -->
					<hr />
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
	import axios from "axios";
	import { Icon } from "@iconify/vue";
	import { NSelect } from "naive-ui";
	import Editor from "@tinymce/tinymce-vue";

	//Mixins
	import errorModalMixin from "../../../mixins/errorModalMixin";
	import iconMixin from "../../../mixins/iconMixin";

	//Validation
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength } from "@vuelidate/validators";
	import ValidationRendering from "../../validation/ValidationRendering.vue";

	//Vuex
	import { mapGetters } from "vuex";

	export default {
		name: "NewRequirementItemWizard",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			editor: Editor,
			Icon,
			NSelect,
			ValidationRendering,
		},
		props: {
			itemStatusList: {
				type: Array,
				default: () => {
					return [];
				},
			},
			itemTypeList: {
				type: Array,
				default: () => {
					return [];
				},
			},
			locationId: {
				type: Number,
				default: 0,
			},
		},
		mixins: [errorModalMixin, iconMixin],
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
				rootUrl: "getRootUrl",
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

				axios
					.post(
						`${this.rootUrl}new_requirement_item/save/${this.locationId}/`,
						data_to_send
					)
					.then((response) => {
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
					})
					.catch((error) => {
						this.showErrorModal(error, this.destination);
					});
			},
		},
		watch: {
			itemStatusList() {
				//We need to transform the data from the JSON array given to one vue-select can read
				this.statusItemFixList = this.itemStatusList.map((row) => {
					return {
						value: row.pk,
						label: row.fields.requirement_item_status,
					};
				});
			},
			itemTypeList() {
				this.typeItemFixList = this.itemTypeList.map((row) => {
					return {
						value: row.pk,
						label: row.fields.requirement_item_type,
					};
				});
			},
		},
	};
</script>

<style scoped></style>
