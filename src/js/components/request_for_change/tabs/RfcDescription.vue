<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Description</h2>
			<p class="text-instructions">
				Place a detailed description here. This should cover what your
				Request For Change (RFC) will entail and why it should be
				implemented within the time frames specified below.
			</p>
		</div>
		<div
			class="col-md-8"
			style="min-height: 610px"
		>
			<div class="form-group">
				<label>
					Request for Change Title:
					<validation-rendering
						v-bind:error-list="v$.rfcTitleModel.$errors"
					></validation-rendering>
				</label>
				<input
					type="text"
					maxlength="255"
					class="form-control"
					v-model="rfcTitleModel"
				/>
			</div>
			<br/>

			<!-- RFC SUMMARY -->
			<label>
				Request for Change Summary:
				<validation-rendering
					v-bind:error-list="v$.rfcSummaryModel.$errors"
				></validation-rendering>
			</label
			><br/>
			<img
				v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
				class="loader-image"
				alt="loading image for Tinymce"
			/>
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
				v-model="rfcSummaryModel"
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
import {mapGetters} from "vuex";

//Composables
import {useNewObjectUploadImage} from "../../../composables/uploads/useNewObjectUploadImage";
import {useUploadImage} from "../../../composables/uploads/useUploadImage";

export default {
	name: "RfcDescription",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		editor: Editor,
		ValidationRendering,
	},
	emits: [
		'update_validation',
		'update_values'
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
	data: () => ({
		rfcSummaryModel: "",
		rfcTitleModel: "",
	}),
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
			staticUrl: "getStaticUrl",
		}),
	},
	validations: {
		rfcSummaryModel: {
			required,
			maxLength: maxLength(630000),
		},
		rfcTitleModel: {
			required,
			maxLength: maxLength(250),
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
				tab: "tab_0",
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
		rfcSummaryModel() {
			this.updateValues("rfcSummaryModel", this.rfcSummaryModel);
			this.updateValidation();
		},
		rfcTitleModel() {
			this.updateValues("rfcTitleModel", this.rfcTitleModel);
			this.updateValidation();
		},
	},
	mounted() {
		//If there is data in the rfcResults - we will update the rfcSummary and rfcTitle
		if (this.rfcResults.length > 0) {
			this.rfcSummaryModel = this.rfcResults[0].fields.rfc_summary;
			this.rfcTitleModel = this.rfcResults[0].fields.rfc_title;
		}

		//Just run the validations to show the error messages
		this.v$.$touch();
	},
};
</script>


