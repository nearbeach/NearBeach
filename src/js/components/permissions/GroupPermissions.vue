<template>
	<div class="row">
		<div class="col-md-4">
			<h2>Group Permissions</h2>
			<p class="text-instructions">
				Add or remove groups from this {{ destination }}. Adding a group
				will allow users from that group to access this
				{{ destination }}.
			</p>
			<p class="text-instructions">
				If you do not add one of your own group(s), you will only get
				readonly access.
			</p>
		</div>
		<div class="col-md-8">
			<label
			>Group List
				<validation-rendering
					v-bind:error-list="v$.groupModel.$errors"
				></validation-rendering>
			</label>
			<n-select
				:options="groupResults"
				label-field="group_name"
      			value-field="group_id"
				label="group"
				v-model:value="groupModel"
				multiple
			></n-select>

			<!-- ALERT FOR WHEN USER GROUPS ARE NOT INCLUDED -->
			<br/>
			<div v-if="displayGroupPermissionIssue"
				class="alert alert-warning"
			>
				You currently don't have enough permissions to create this object. Please select groups where you have
				the create ability.
			</div>
		</div>
	</div>
</template>

<script>
import {NSelect} from "naive-ui";

//Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";
import ValidationRendering from "../validation/ValidationRendering.vue";

export default {
	name: "GroupPermissions",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		NSelect,
		ValidationRendering,
	},
	emits: ['update_group_model'],
	props: {
		destination: {
			type: String,
			default: "",
		},
		displayGroupPermissionIssue: {
			type: Boolean,
			default: false,
		},
		groupResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		userGroupPermissions: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
	watch: {
		groupModel() {
			//Send the data upstream
			this.$emit("update_group_model", this.groupModel);
		},
	},
	data() {
		return {
			groupModel: [],
		};
	},
	validations: {
		groupModel: {
			required,
		},
	},
	mounted() {
		//Any User groups are added to the group Model
		this.groupModel = this.userGroupPermissions.map((row) => {
			return row.group_id;
		});
	},
};
</script>


