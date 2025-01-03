<template>
	<div v-if="uploadState === 'before_upload'"
		 class="row"
	>
		<div class="col-md-4">
			<strong>Upload Document Test</strong>
			<p class="text-instructions">
				Please click on the "Upload Document" button. It will upload a small text file to the blob storage. If
				there are any issues, they will print here.
			</p>
		</div>
		<div class="col-md-8">
			<button class="btn btn-primary"
					v-on:click="uploadFile"
			>
				Upload Test
			</button>

			<div v-if="uploadIssues !== ''"
				class="alert alert-danger"
			>
				<h1>Upload Issues</h1>
				{{ uploadIssues }}
			</div>
		</div>
	</div>
	<div v-else-if="uploadState === 'sending'">
		<div class="alert alert-info">Currently sending data</div>
	</div>
	<div v-else-if="uploadState === 'error'">
		<div class="alert alert-danger">
			Sorry this upload process failed. Please read the error below.
		</div>
		<iframe :srcdoc="uploadError"></iframe>
	</div>
	<div v-else
		 class="row"
	>
		<div class="col-md-4">
			<strong>Test Download</strong>
			<p class="text-instructions">
				Please download the file and compare it's components with the UUID. They should match.
			</p>
		</div>
		<div class="col-md-8">
			<p><a v-bind:href="downloadLocation" target="_blank" rel="noopener noreferrer">Please click here to download the file.</a></p>
			<p>It's contents should match the UUID: {{ uuidVerification }}</p>
		</div>
	</div>
</template>

<script>
//VueX
import { mapGetters } from "vuex";

//Composables
import {useRandomID} from "../../composables/security/useRandomID";

export default {
	name: "DiagnosticUpload",
	data() {
		return {
			downloadLocation: "",
			uploadError: "",
			uploadIssues: "",
			uploadState: "before_upload",
			uuidVerification: "",
		}
	},
	computed: {
		...mapGetters({
			rootUrl: 'getRootUrl',
		})
	},
	methods: {
		uploadFile() {
			//State changes
			this.uploadState = "sending";

			//Create a simple uuid
			const uuid = useRandomID();

			//Create the file we are uploading
			const document = new Blob([uuid], { type: "text/plain"});

			//Create the form data
			const data_to_send = new FormData();
			data_to_send.set(
				'document',
				document,
				'diagnostic-upload-test.txt',
			);
			data_to_send.set("uuid", uuid.toString());

			this.axios.post(
				`${this.rootUrl}diagnostic_information/upload_test/`,
				data_to_send,
			).then((response) => {
				this.uploadState = "Completed";
				this.uuidVerification = uuid;
				this.downloadLocation = `${this.rootUrl}private/${response.data[0].document_key_id}/`
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Error with Uploads",
					message: `Sorry could not upload document. Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});

				this.uploadState = "error";
				this.uploadError = error.response.data;
			})
		}
	}
}
</script>