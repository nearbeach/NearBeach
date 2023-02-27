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
					<span
						class="error"
						v-if="
							!v$.rfcTitleModel.required &&
							v$.rfcTitleModel.$dirty
						"
					>
						Please suppy a title.</span
					>
				</label>
				<input
					type="text"
					maxlength="255"
					class="form-control"
					v-model="rfcTitleModel"
				/>
			</div>
			<br />

			<!-- RFC SUMMARY -->
			<label
				>Request for Change Summary:
				<span
					class="error"
					v-if="
						!v$.rfcSummaryModel.required &&
						v$.rfcSummaryModel.$dirty
					"
				>
					Please supply a description.</span
				>
				<span
					class="error"
					v-if="!v$.rfcSummaryModel.maxLength"
				>
					Sorry - too many characters.</span
				> </label
			><br />
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
				v-model="rfcSummaryModel"
			/>
		</div>
	</div>
</template>

<script>
	//Validations
	import useVuelidate from "@vuelidate/core";
	import { required, maxLength } from "@vuelidate/validators";
	import Editor from "@tinymce/tinymce-vue";

	//Mixins
	import uploadMixin from "../../../mixins/uploadMixin";

	//VueX
	import { mapGetters } from "vuex";

	export default {
		name: "RfcDescription",
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
				default() {
					return [];
				},
			},
		},
		mixins: [uploadMixin],
		data: () => ({
			rfcSummaryModel: "",
			rfcTitleModel: "",
		}),
		computed: {
			...mapGetters({
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
			updateValues(modelName, modelValue) {
				this.$emit("update_values", {
					modelName: modelName,
					modelValue: modelValue,
				});
			},
		},
		watch: {
			rfcSummaryModel() {
				this.updateValues("rfcSummaryModel", this.rfcSummaryModel);
			},
			rfcTitleModel() {
				this.updateValues("rfcTitleModel", this.rfcTitleModel);
			},
		},
		updated() {
			this.v$.$touch();

			this.$emit("update_validation", {
				tab: "tab_0",
				value: !this.v$.$invalid,
			});
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

<style scoped></style>
