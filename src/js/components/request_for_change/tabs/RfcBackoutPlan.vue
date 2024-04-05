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
			<label>
				Backout Plan:
				<validation-rendering
					v-bind:error-list="v$.rfcBackoutPlanModel.$errors"
				></validation-rendering>
			</label>
			<br/>
			<editor
				:init="{
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
				}"
				v-bind:disabled="isReadOnly"
				v-model="rfcBackoutPlanModel"
			/>
		</div>
	</div>
</template>

<script>
//Validation
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "../../validation/ValidationRendering.vue";

//TinyMce Editor
import Editor from "@tinymce/tinymce-vue";

//Mixins
import uploadMixin from "../../../mixins/uploadMixin";
import newObjectUploadMixin from "../../../mixins/newObjectUploadMixin";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "RfcBackoutPlan",
	setup() {
		return {v$: useVuelidate()};
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
	mixins: [uploadMixin, newObjectUploadMixin],
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
		handleUploadImage(blobInfo, progress) {
			//If we have passed a UUID down, this is a new object
			//We'll need to use the new object upload
			//Otherwise use the usual method
			if (this.uuid === "") return this.uploadImage(blobInfo, progress);
			return this.newObjectUploadImage(blobInfo, progress)
		},
		updateValidation() {
			this.v$.$touch();

			this.$emit("update_validation", {
				tab: "tab_4",
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
		rfcBackoutPlanModel() {
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

		//Just run the validations to show the error messages
		this.v$.$touch();
	},
};
</script>

<style scoped></style>
