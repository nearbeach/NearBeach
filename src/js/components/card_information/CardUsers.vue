<template>
	<render-user-card-list
		v-bind:object-user-list="objectUserList"
		v-on:remove_user="removeUser"
	></render-user-card-list>

	<div
		class="row mt-3"
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

//Vuex components
import {mapGetters} from "vuex";
import RenderUserCardList from "../render/RenderUserCardList.vue";

export default {
	name: "CardUsers",
	components: {
		RenderUserCardList,
	},
	computed: {
		...mapGetters({
			cardId: "getCardId",
			kanbanBoardStatus: "getKanbanStatus",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			staticUrl: "getStaticUrl",
			userLevel: "getUserLevel",
			objectUserList: "getObjectUserList",
		}),
	},
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
					`${this.rootUrl}object_data/kanban_card/${this.cardId}/remove_user/`,
					data_to_send
				)
				.then((response) => {
					//Update VueX with the required data
					this.$store.commit("updateGroupsAndUsers", {
						objectGroupList: response.data.object_group_list,
						objectUserList: response.data.object_user_list,
						potentialGroupList: response.data.potential_group_list,
						potentialUserList: response.data.potential_user_list,
						userGroupList: response.data.user_group_list,
					})
				});
		},
	},
};
</script>
