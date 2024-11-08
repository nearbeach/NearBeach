<template>
	<n-config-provider :theme="useNBTheme(theme)">
		<div class="card">
			<div class="card-body">
				<h1>Diagnostic Information</h1>
				<hr/>

				<h2>Core Configurations</h2>

				<div class="spacer"></div>

				<div class="row">
					<div class="col-md-4">
						<strong>Azure Storage</strong>
						<p class="text-instructions">
							Confirms these values have been set in your Django Settings file. Please ignore if you are
							not utilsing Azure Storage
						</p>
					</div>
					<div class="col-md-8">
						<table class="table">
							<thead>
								<tr>
									<td style="width:80%">Configuration Field</td>
									<td style="width:20%">Is Filled In</td>
								</tr>
							</thead>
							<tbody>
								<tr>
									<td>AZURE_STORAGE_CONNECTION_STRING</td>
									<td>{{ azureStorageConnectionString }}</td>
								</tr>
								<tr>
									<td>AZURE_STORAGE_CONTAINER_NAME</td>
									<td>{{ azureStorageContainerName }}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<hr/>

				<div class="row">
					<div class="col-md-4">
						<strong>S3/R2/Minio Storage</strong>
						<p class="text-instructions">
							Confirms these values have been set in your Django Settings file. Please ignore if you are
							not utilsing either S3, R2, or Minio storage solutions.
						</p>
					</div>
					<div class="col-md-8">
						<table class="table">
							<thead>
							<tr>
								<td style="width:80%">Configuration Field</td>
								<td style="width:20%">Is Filled In</td>
							</tr>
							</thead>
							<tbody>
							<tr>
								<td>AWS_ACCESS_KEY_ID</td>
								<td>{{ awsAccessKeyId }}</td>
							</tr>
							<tr>
								<td>AWS_SECRET_ACCESS_KEY</td>
								<td>{{ awsSecretAccessKey }}</td>
							</tr>
							<tr>
								<td>AWS_S3_ENDPOINT_URL (for minio)</td>
								<td>{{ awsS3EndpointUrl }}</td>
							</tr>
							<tr>
								<td>AWS_STORAGE_BUCKET_NAME</td>
								<td>{{ awsStorageBucketName }}</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>

				<hr/>

				<div class="row">
					<div class="col-md-4">
						<strong>Email</strong>
						<p class="text-instructions">
							Confirms these values have been set in your Django Settings file.
						</p>
					</div>
					<div class="col-md-8">
						<table class="table">
							<thead>
							<tr>
								<td style="width:80%">Configuration Field</td>
								<td style="width:20%">Values</td>
							</tr>
							</thead>
							<tbody>
							<tr>
								<td>SMTP_EMAIL_HOST</td>
								<td>{{ smtpEmailHost }}</td>
							</tr>
							<tr>
								<td>SMTP_EMAIL_HOST_USER</td>
								<td>{{ smtpEmailHostUser }}</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>

				<hr/>

				<div class="row">
					<div class="col-md-4">
						<strong>Allowed Hosts & CSRF Trusted URLS</strong>
						<p class="text-instructions">
							Confirms these values have been set in your Django Settings file.
						</p>
					</div>
					<div class="col-md-8">
						<table class="table">
							<thead>
							<tr>
								<td style="width:50%">Configuration Field</td>
								<td style="width:50%">Is Filled In</td>
							</tr>
							</thead>
							<tbody>
							<tr>
								<td>ALLOWED_HOSTS</td>
								<td>
									<p v-for="single in allowedHosts"
									   :key="single"
									>- {{ single }}</p>
								</td>
							</tr>
							<tr>
								<td>CSRF_TRUSTED_URLS</td>
								<td>
									<p v-for="single in allowedHosts"
									   :key="single"
									>- {{ single }}</p>
								</td>
							</tr>
							</tbody>
						</table>
					</div>
				</div>

				<hr/>

				<diagnostic-upload></diagnostic-upload>

				<hr/>

				<diagnostic-email-test></diagnostic-email-test>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
//Components
import DiagnosticUpload from "./DiagnosticUploadTest.vue";
import DiagnosticEmailTest from "./DiagnosticEmailTest.vue";
import {useNBTheme} from "../../composables/theme/useNBTheme";

export default {
	name: "DiagnosticInformation",
	components: {
		DiagnosticEmailTest,
		DiagnosticUpload
	},
	props: {
		awsAccessKeyId: {
			type: Boolean,
			default: false,
		},
		awsSecretAccessKey: {
			type: Boolean,
			default: false,
		},
		allowedHosts: {
			type: Array,
			default: () => {
				return [];
			},
		},
		awsS3EndpointUrl: {
			type: Boolean,
			default: false,
		},
		awsStorageBucketName: {
			type: Boolean,
			default: false,
		},
		azureStorageConnectionString: {
			type: Boolean,
			default: false,
		},
		azureStorageContainerName: {
			type: Boolean,
			default: false,
		},
		rootUrl: {
			type: String,
			default: "/",
		},
		smtpEmailHost: {
			type: Boolean,
			default: false,
		},
		smtpEmailHostUser: {
			type: Boolean,
			default: false,
		},
		theme: {
			type: String,
			default: "light",
		},
	},
	methods: {useNBTheme},
	mounted() {
		this.$store.commit({
			type: "updateUrl",
			rootUrl: this.rootUrl,
		});
	}
}
</script>