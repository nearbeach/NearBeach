<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Backout Plan</h2>
			<p class="text-instructions">
				Please outline the backout plan that will be implemented, and
				when it will be implemented, when something goes wrong with the
				Request for Change.
			</p>
		</div>
		<div
			class="col-md-8"
			style="min-height: 610px"
		>
			<label
				>Backout Plan:
				<span
					class="error"
					v-if="
						!v$.rfcBackoutPlanModel.required &&
						v$.rfcBackoutPlanModel.$dirty
					"
				>
					Please supply a description.</span
				>
				<span
					class="error"
					v-if="!v$.rfcBackoutPlanModel.maxLength"
				>
					Sorry - too many characters.</span
				> </label
			><br />
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
				v-model="rfcBackoutPlanModel"
			/>
		</div>
	</div>
</template>

<script>
	//Validation
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength } from "@vuelidate/validators";

	//TinyMce Editor
	import Editor from "@tinymce/tinymce-vue";

	//Mixins
	import uploadMixin from "../../../mixins/uploadMixin";

	export default {
		name: "RfcBackoutPlan",
		setup() {
			return { v$: useVuelidate() };
		},
		components: {
			editor: Editor,
		},
		props: {
			isReadOnly: {
				type: Boolean,
				default: false,
			},
			rfcResults: {
				type: Array,
				default: function () {
					return [];
				},
			},
		},
		mixins: [uploadMixin],
		data: () => ({
			rfcBackoutPlanModel: "",
		}),
		validations: {
			rfcBackoutPlanModel: {
				required,
				maxLength: maxLength(630000),
			},
		},
		methods: {
			updateValidation: function () {
				this.v$.$touch();

				this.$emit("update_validation", {
					tab: "tab_4",
					value: !this.v$.$invalid,
				});
			},
			updateValues: function (modelName, modelValue) {
				this.$emit("update_values", {
					modelName: modelName,
					modelValue: modelValue,
				});
			},
		},
		watch: {
			rfcBackoutPlanModel: function () {
				this.updateValues("rfcBackoutPlan", this.rfcBackoutPlanModel);
				this.updateValidation();
			},
		},
		mounted() {
			//If the rfc results import - update the rfcBackout Model
			if (this.rfcResults.length > 0) {
				this.rfcBackoutPlanModel =
					this.rfcResults[0].fields.rfc_backout_plan;
			}
		},
	};
</script>

<style scoped></style>
