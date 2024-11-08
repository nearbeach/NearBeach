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
			<br/>
			<editor
				license-key="gpl"
				:init="{
					license_key: 'gpl',
					file_picker_types: 'image',
					height: 500,
					images_upload_handler: handleUploadImage,
					menubar: false,
					paste_data_images: true,
					plugins: ['lists', 'image', 'codesample', 'table'],
            		toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 		 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
					skin: `${this.skin}`,
					content_css: `${this.contentCss}`,
					relative_urls: false,
				}"
				v-bind:disabled="isReadOnly"
				v-model="rfcImplementationPlanModel"
			/>
		</div>
	</div>
</template>

<script>
//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../../validation/ValidationRendering.vue";

//TinyMce
import Editor from "@tinymce/tinymce-vue";

//VueX
import { mapGetters } from "vuex";
import {useNewObjectUploadImage} from "../../../composables/uploads/useNewObjectUploadImage";
import {useUploadImage} from "../../../composables/uploads/useUploadImage";

export default {
	name: "RfcImplementationPlan",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		ValidationRendering,
	},
	emits: [
		'update_values',
		'update_validation',
	],
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
		uuid: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
		})
	},
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
		handleUploadImage(blobInfo, progress) {
			//If we have passed a UUID down, this is a new object
			//We'll need to use the new object upload
			//Otherwise use the usual method
			if (this.uuid === "") return useUploadImage(blobInfo, progress);
			return useNewObjectUploadImage(blobInfo, progress)
		},
		updateValidation() {
			this.v$.$touch();

			this.$emit("update_validation", {
				tab: "tab_3",
				value: !this.v$.$invalid,
			});
		},
		updateValues(modelName, modelValue) {
			this.$emit("update_values", {
				modelName,
				modelValue,
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

		//Just run the validations to show the error messages
		this.v$.$touch();
	},
};
</script>


