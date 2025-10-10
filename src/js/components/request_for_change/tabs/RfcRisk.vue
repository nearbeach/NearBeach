<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Risk</h2>
			<p class="text-instructions">
				Please outline all risks associated with this Request for
				Change. A detail list of all risks should be noted.
			</p>
		</div>

		<div
			class="col-md-8"
			style="min-height: 610px"
		>
			<div class="row">
				<div class="col-md-4">
					<label>
						Priority of Change
						<validation-rendering
							:error-list="v$.rfcPriorityModel.$errors"
						></validation-rendering>
					</label>
					<n-select
						v-model:value="rfcPriorityModel"
						:options="rfcPriority"
						:disabled="isReadOnly"
					></n-select>
				</div>
				<div class="col-md-4">
					<label>
						Risk of Change
						<validation-rendering
							:error-list="v$.rfcRiskModel.$errors"
						></validation-rendering>
					</label>
					<n-select
						v-model:value="rfcRiskModel"
						:options="rfcRisk"
						:disabled="isReadOnly"
					></n-select>
				</div>
				<div class="col-md-4">
					<label>
						Impact of Change
						<validation-rendering
							:error-list="v$.rfcImpactModel.$errors"
						></validation-rendering>
					</label>
					<n-select
						v-model:value="rfcImpactModel"
						:options="rfcImpact"
						:disabled="isReadOnly"
					></n-select>
				</div>
			</div>
			<br/>

			<!-- RFC SUMMARY -->
			<label>
				Risk Association:
				<validation-rendering
					:error-list="v$.rfcRiskSummaryModel.$errors"
				></validation-rendering>
			</label>
			<br/>
			<editor
				v-model="rfcRiskSummaryModel"
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
					skin: `${skin}`,
					content_css: `${contentCss}`,
					relative_urls: false,
				}"
				:disabled="isReadOnly"
			/>
		</div>
	</div>
</template>

<script>
//Validations
import useVuelidate from "@vuelidate/core";
import {required, maxLength} from "@vuelidate/validators";
import ValidationRendering from "Components/validation/ValidationRendering.vue";

//Widgets
import {NSelect} from "naive-ui";
import Editor from "@tinymce/tinymce-vue";

//VueX
import { mapGetters } from "vuex";
import {useNewObjectUploadImage} from "Composables/uploads/useNewObjectUploadImage";
import {useUploadImage} from "Composables/uploads/useUploadImage";

export default {
	name: "RfcRisk",
	components: {
		editor: Editor,
		NSelect,
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
	emits: [
		'update_values',
		'update_validation',
	],
	setup() {
		return {v$: useVuelidate()};
	},
	data: () => ({
		rfcPriority: [
			{label: "Critical", value: 4},
			{label: "High", value: 3},
			{label: "Medium", value: 2},
			{label: "Low", value: 1},
		],
		rfcPriorityModel: "",
		rfcRisk: [
			{label: "Very High", value: 5},
			{label: "High", value: 4},
			{label: "Moderate", value: 3},
			{label: "Low", value: 2},
			{label: "None", value: 1},
		],
		rfcRiskModel: "",
		rfcRiskSummaryModel: "",
		rfcImpact: [
			{label: "High", value: 3},
			{label: "Medium", value: 2},
			{label: "Low", value: 1},
		],
		rfcImpactModel: "",
	}),
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
		}),
	},
	validations: {
		rfcPriorityModel: {
			required,
		},
		rfcRiskModel: {
			required,
		},
		rfcRiskSummaryModel: {
			required,
			maxLength: maxLength(630000),
		},
		rfcImpactModel: {
			required,
		},
	},
	watch: {
		rfcPriority() {
			this.updateValues("rfcPriority", this.rfcPriority);
			this.updateValidation();
		},
		rfcPriorityModel() {
			this.updateValues("rfcPriorityModel", this.rfcPriorityModel);
			this.updateValidation();
		},
		rfcRisk() {
			this.updateValues("rfcRisk", this.rfcRisk);
			this.updateValidation();
		},
		rfcRiskModel() {
			this.updateValues("rfcRiskModel", this.rfcRiskModel);
			this.updateValidation();
		},
		rfcRiskSummaryModel() {
			this.updateValues(
				"rfcRiskSummaryModel",
				this.rfcRiskSummaryModel
			);
			this.updateValidation();
		},
		rfcImpact() {
			this.updateValues("rfcImpact", this.rfcImpact);
			this.updateValidation();
		},
		rfcImpactModel() {
			this.updateValues("rfcImpactModel", this.rfcImpactModel);
			this.updateValidation();
		},
	},
	mounted() {
		//When template loads - check to see if there is any data within the rfcResults. If so -> update all models
		if (this.rfcResults.length > 0) {
			// Filter for the correct rfcPriority
			this.rfcPriorityModel = this.rfcResults[0].fields.rfc_priority;

			//Filter for the correct rfcRisk
			this.rfcRiskModel = this.rfcResults[0].fields.rfc_risk;

			this.rfcRiskSummaryModel =
				this.rfcResults[0].fields.rfc_risk_and_impact_analysis;

			//Filter for the correct rfc Impact
			this.rfcImpactModel = this.rfcResults[0].fields.rfc_impact;
		}

		//Just run the validations to show the error messages
		this.v$.$touch();
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
				tab: "tab_2",
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
};
</script>


