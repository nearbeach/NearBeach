<template>
	<n-config-provider :theme="getTheme(theme)">
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
						<br/>
						<n-upload
							:action="`${rootUrl}profile_information/update_profile/`"
							:headers="{
							'X-CSRFTOKEN': getToken('csrftoken'),
						}"
							:data="{}"
							:max="1"
							@error="showErrorToast"
							@finish="updateProfilePicture"
						>
							<n-button>Update Profile Picture</n-button>
						</n-upload>
					</div>
				</div>
			</div>
		</div>
	</n-config-provider>
</template>

<script>
import {NUpload, NButton} from "naive-ui";
import {mapGetters} from "vuex";

//Mixins
import getToken from "../../mixins/getTokenMixin";
import getThemeMixin from "../../mixins/getThemeMixin";

export default {
	name: "UpdateProfilePicture",
	components: {
		NButton,
		NUpload,
	},
	props: {
		theme: {
			type: String,
			default: "",
		},
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
	mixins: [getToken, getThemeMixin],
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
		showErrorToast(data) {
			this.$store.dispatch("newToast", {
				header: "Can not update profile picture",
				message: data.event.target.responseText,
				extra_classes: "bg-danger",
				delay: 0,
			});
		},
		updateProfilePicture() {
			//Contact the API to get the location of the new image
			this.axios
				.get(
					"get_profile_picture/",
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
