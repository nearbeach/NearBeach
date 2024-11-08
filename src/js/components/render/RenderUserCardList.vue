<template>
	<div v-if="loadingData"
		class="alert alert-info"
	>
		Currently loading User Data.
	</div>
	<div
		v-else-if="objectUserList.length === 0 && !addingUserStatus"
		class="alert alert-dark"
	>
		Sorry, there are no users currently assigned to this object.
	</div>
	<div
		v-else
		class="user-card-list"
	>
		<div
			v-for="user in objectUserList"
			v-bind:key="user.username"
			class="user-card"
		>
			<img
				v-bind:src="profilePicture(user.profile_picture)"
				alt="default profile"
				class="user-card--profile"
			/>
			<div class="user-card--details">
				<div class="user-card--name">
					{{ user.first_name }} {{ user.last_name }}
				</div>
				<div class="user-card--email">
					{{ user.email }}
				</div>
			</div>
			<div
				class="user-card--remove"
				v-if="userLevel >= 3"
			>
				<carbon-trash-can
					v-on:click="removeUser(user.username)"
				></carbon-trash-can>
			</div>
		</div>
		<div v-if="addingUserStatus"
			 class="user-card"
		>
			<div class="user-card--details">++ Adding User(s) ++</div>
		</div>
	</div>

</template>

<script>
//VueX
import { mapGetters } from "vuex";
import {CarbonTrashCan} from "../../components";

export default {
	name: "RenderUserCardList",
	components: {
		CarbonTrashCan,
	},
	emits: [
		'remove_user',
	],
	props: {
		addingUserStatus: {
			type: Boolean,
			default: false,
		},
		loadingData: {
			type: Boolean,
			default: false,
		},
		objectUserList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "") {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
		removeUser(username) {
			this.$emit("remove_user", username);
		},
	}
}
</script>