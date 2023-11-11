<template>
	<div
		class="alert alert-secondary"
		v-if="objectUserList.length === 0"
	>
		Sorry, there are no users currently assigned to this card.
	</div>
	<div v-else>
		<table class="table">
			<thead>
			<tr>
				<td scope="col">Username</td>
				<td scope="col">Name</td>
				<td
					scope="col"
					v-if="userLevel === 4"
				>
					Delete
				</td>
			</tr>
			</thead>
			<tbody>
			<tr
				v-for="user in objectUserList"
				v-bind:key="user.id"
			>
				<td>{{ user.id }} - {{ user.username }}</td>
				<td>{{ user.first_name }} {{ user.last_name }}</td>
				<td v-if="userLevel >= 2">
					<Icon
						v-bind:icon="icons.trashCan"
						v-on:click="removeUser(user.username)"
					/>
				</td>
			</tr>
			</tbody>
		</table>
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
