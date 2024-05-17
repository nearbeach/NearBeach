<template>
	<div
		class="alert alert-secondary"
		v-if="objectUserList.length === 0"
	>
		Sorry, there are no users currently assigned to this card.
	</div>
	<div v-else
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
				<Icon
					v-bind:icon="icons.trashCan"
					v-on:click="removeUser(user.username)"
				/>
			</div>
		</div>

	</div>
	<div
		class="row"
		v-if="userLevel > 1 && kanbanBoardStatus !== 'Closed'"
	>
		<div class="col-md-12">
			<button
				class="btn btn-primary"
				v-on:click="addUser"
			>
				Add User
			</button>
		</div>
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";

//Vuex components
import {mapGetters} from "vuex";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "CardUsers",
	components: {
		Icon,
	},
	computed: {
		...mapGetters({
			cardId: "getCardId",
			kanbanBoardStatus: "getKanbanStatus",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
			objectUserList: "getObjectUserList",
		}),
	},
	mixins: [iconMixin],
	methods: {
		addUser() {
			//Close the current modal
			document
				.getElementById("cardInformationModalCloseButton")
				.click();

			//Open the user wizard model
			const addUserWizard = new Modal("#addUserModal");
			addUserWizard.show();
		},
		profilePicture(picture_uuid) {
			if (picture_uuid !== null && picture_uuid !== "") {
				return `${this.rootUrl}private/${picture_uuid}/`;
			}

			return `${this.staticUrl}NearBeach/images/placeholder/people_tax.svg`;
		},
		removeUser(username) {
			//Data to send
			const data_to_send = new FormData();
			data_to_send.set("username", username);

			//Axios
			this.axios
				.post(
					`${this.rootUrl}object_data/kanban_card/${this.locationId}/remove_user/`,
					data_to_send
				)
				.then((response) => {
					//Update VueX with the required data
					this.$store.commit("updateGroupsAndUsers", {
						objectGroupList: response.data.object_group_list,
						objectUserList: response.data.object_user_list,
						potentialGroupList: response.data.potential_group_list,
						potentialUserList: response.data.potential_user_list,
					})
				});
		},
	},
};
</script>
