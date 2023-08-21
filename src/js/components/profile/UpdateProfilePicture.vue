<template>
	<div class="card">
		<div class="card-body">
			<div class="row">
				<div class="col-md-4">
					<strong>Update Profile Picture</strong>
					<p class="text-instructions">
						Click on "Update Picture" to update your profile picture
					</p>
				</div>
				<div class="col-md-3">
					<img
						v-bind:src="profilePicture"
						alt="Profile Picture"
						class="organisation-profile-image"
					/>
					<br />
					<!--<button class="btn btn-primary">Update Profile...</button>-->
					<n-upload
						:action="`${rootUrl}profile_information/update_profile/`"
						:headers="{
							'X-CSRFTOKEN': getToken('csrftoken'),
						}"
						:data="{}"
						@finish="updateProfilePicture"
					>
						<n-button>Update Profile Picture</n-button>
					</n-upload>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	import { NUpload, NButton } from "naive-ui";
	import { mapGetters } from "vuex";
	import getToken from "../../mixins/getTokenMixin";

	const axios = require('axios');

	export default {
		name: "UpdateProfilePicture",
		components: {
			NButton,
			NUpload,
		},
		props: {
			userProfile: {
				type: Array,
				default: () => {
					return [];
				},
			},
		},
		data: () => ({
			profilePicture: "",
		}),
		computed: {
			...mapGetters({
				staticUrl: "getStaticUrl",
				rootUrl: "getRootUrl",
			}),
		},
		mixins: [getToken],
		methods: {
			setProfilePicture() {
				//Set the default
				this.profilePicture = `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`;

				//Escape
				if (this.userProfile.length === 0) return;

				//Run through the conditions of not using the default profile
				let profile_picture = this.userProfile[0].fields.document;
				if (
					profile_picture !== undefined &&
					profile_picture !== null &&
					profile_picture !== ""
				) {
					//There is a profile image
					this.profilePicture = `${this.rootUrl}private/${profile_picture}`;
				}
			},
			updateProfilePicture() {
				//Contact the API to get the location of the new image
				axios
					.get(
						`get_profile_picture/`,
						{}
					)
					.then((response) => {
						this.profilePicture = `${this.rootUrl}private/${response.data.profile_picture}`;
					})
					.catch(() => {
						this.profilePicture = `${this.staticUrl}/NearBeach/images/placeholder/product_tour.svg`;
					});
			},
		},
		mounted() {
			//Get the profile picture
			this.setProfilePicture();
		},
	};
</script>
