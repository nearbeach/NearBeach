<template>
	<h2>Description</h2>
	<p class="text-instructions">
		The description is optional. If you update the
		description, please hit the "Update Descritpion" button
	</p>
	<editor
		:init="{
            file_picker_types: 'image',
            height: 300,
            images_upload_handler: customUploadImage,
            menubar: false,
            paste_data_images: true,
            plugins: ['lists', 'image', 'codesample', 'table'],
            toolbar: [
                'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                'bold italic strikethrough underline backcolor | table | ' +
                    'bullist numlist outdent indent | removeformat | image codesample',
            ],
        }"
		v-bind:content_css="false"
		v-bind:skin="false"
		v-model="changeDescriptionModel"
	/>

	<hr/>
	<div class="row submit-row">
		<div class="col-md-12">
			<button
				class="btn btn-primary save-changes"
				v-on:click="updateDescription"
			>
				Update Description
			</button>
		</div>
	</div>
</template>

<script>
import axios from "axios";
import Editor from "@tinymce/tinymce-vue";

export default {
	name: "ChangeTaskDescription",
	components: {
		Editor,
	},
	computed: {
		changeDescriptionModel: {
			get() {
				return this.$store.state.changeTask.description;
			},
			set(changeDescription) {
				this.$store.commit({
					type: "updateChangeTaskDescription",
					changeTaskDescription: changeDescription,
				});
			}
		}
	},
	methods: {
		customUploadImage(blobInfo, success, failure, progress) {
			//Create the form
			const data_to_send = new FormData();
			data_to_send.set(
				"document",
				blobInfo.blob(),
				blobInfo.filename()
			);
			data_to_send.set("document_description", blobInfo.filename());

			//Configuration for axios
			const config = {
				onUploadProgress: (progressEvent) => {
					//As the document gets uploaded - we want to update the upload Percentage
					progress =
						parseFloat(progressEvent.loaded) /
						parseFloat(progressEvent.total);
				},
			};

			//Create url
			const url = `${this.rootUrl}documentation/request_for_change/${this.changeTaskResults[0].fields.request_for_change}/upload/`;

			//Use axios to send the data
			axios
				.post(url, data_to_send, config)
				.then((response) => {
					//Just send the location to the success
					success(`/private/${response.data[0].document_key_id}`);
				})
				.catch((error) => {
				});
		},
		updateDescription() {
			const data_to_send = new FormData();
			data_to_send.set('change_task_description', this.changeDescriptionModel);

			axios.post(
				`update/description/`,
				data_to_send,
			).then((response) => {

			})
				.catch((error) => {
				})
		},
	}
}
</script>