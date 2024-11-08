<template>
	<h2>Description</h2>
	<p class="text-instructions">
		The description is optional. If you update the
		description, please hit the "Update Descritpion" button
	</p>
	<editor
		license-key="gpl"
		:init="{
			license_key: 'gpl',
            file_picker_types: 'image',
            height: 300,
            images_upload_handler: customUploadImage,
            menubar: false,
            paste_data_images: true,
            plugins: ['lists', 'image', 'codesample', 'table'],
            toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            skin: `${this.skin}`,
            content_css: `${this.contentCss}`,
            relative_urls: false,
        }"
		v-model="changeDescriptionModel"
		v-bind:disabled="isReadOnly"
	/>

	<hr v-if="!isReadOnly"/>
	<div
		class="row submit-row"
		v-if="!isReadOnly"
	>
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
import Editor from "@tinymce/tinymce-vue";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "ChangeTaskDescription",
	components: {
		Editor,
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			isReadOnly: "getIsChangeTaskReadOnly",
			skin: "getSkin",
		}),
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
		customUploadImage(blobInfo, success) {
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
				onUploadProgress: () => {
					//As the document gets uploaded - we want to update the upload Percentage
					
				},
			};

			//Create url
			const url = `${this.rootUrl}documentation/request_for_change/${this.changeTaskResults[0].fields.request_for_change}/upload/`;

			//Use axios to send the data
			this.axios.post(
				url,
				data_to_send, config
			).then((response) => {
				//Just send the location to the success
				success(`/private/${response.data[0].document_key_id}`);
			
			});
		},
		updateDescription() {
			this.$store.dispatch("newToast", {
				header: "Updating Description",
				message: "Updating Description, please wait",
				extra_classes: "bg-warning text-dark",
				delay: 0,
				unique_type: "save_description",
			});

			const data_to_send = new FormData();
			data_to_send.set('change_task_description', this.changeDescriptionModel);

			this.axios.post(
				"update/description/",
				data_to_send,
			).then(() => {
				this.$store.dispatch("newToast", {
					header: "Updated Description",
					message: "Description Updated",
					extra_classes: "bg-success",
					unique_type: "save_description",
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed Updating Description",
					message: `Sorry - description failed to update. Error -> ${error}`,
					extra_classes: "bg-warning text-dark",
					delay: 0,
					unique_type: "save_description",
				});
			});
		},
	},
}
</script>