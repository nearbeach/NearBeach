<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Implementation Plan</h2>
			<p class="text-instructions">
				Please outline your implementation plan for this request for
				change.
			</p>
		</div>
		<div
			class="col-md-8"
			style="min-height: 610px"
		>
			<label>
				Implementation Plan:
				<validation-rendering
					v-bind:error-list="v$.rfcImplementationPlanModel.$errors"
				></validation-rendering>
			</label>
			<br />
			<editor
				:init="{
					file_picker_types: 'image',
					height: 500,
					images_upload_handler: uploadImage,
					menubar: false,
					paste_data_images: true,
					plugins: ['lists', 'paste', 'table'],
					toolbar: [
						'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
						'bold italic strikethrough underline backcolor | table | ' +
							'bullist numlist outdent indent | removeformat',
					],
				}"
				v-bind:content_css="false"
				v-bind:skin="false"
				v-bind:disabled="isReadOnly"
				v-model="rfcImplementationPlanModel"
			/>
		</div>
	</div>
</template>

<script>
	//Validations
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength } from "@vuelidate/validators";
	import ValidationRendering from "../../validation/ValidationRendering.vue";

	//TinyMce
	import Editor from "@tinymce/tinymce-vue";

	//Mixins
	import uploadMixin from "../../../mixins/uploadMixin";

	export default {
		name: "RfcImplementationPlan",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			editor: Editor,
			ValidationRendering,
		},
		props: {
			isReadOnly: {
				type: Boolean,
				default: false,
			},
			rfcResults: {
				type: Array,
				default() {
					return [];
				},
			},
		},
		mixins: [uploadMixin],
		data: () => ({
			rfcImplementationPlanModel: "",
		}),
		validations: {
			rfcImplementationPlanModel: {
				required,
				maxLength: maxLength(630000),
			},
		},
		methods: {
			updateValidation() {
				this.v$.$touch();

				this.$emit("update_validation", {
					tab: "tab_3",
					value: !this.v$.$invalid,
				});
			},
			updateValues(modelName, modelValue) {
				this.$emit("update_values", {
					modelName: modelName,
					modelValue: modelValue,
				});
			},
		},
		watch: {
			rfcImplementationPlanModel() {
				this.updateValues(
					"rfcImplementationPlanModel",
					this.rfcImplementationPlanModel
				);
				this.updateValidation();
			},
		},
		mounted() {
			//If the rfcResults are imported, update the rfcImplementationPlan
			if (this.rfcResults.length > 0) {
				this.rfcImplementationPlanModel =
					this.rfcResults[0].fields.rfc_implementation_plan;
			}
		},
	};
</script>

<style scoped></style>
