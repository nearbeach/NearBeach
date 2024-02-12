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
				:options="groupFixResults"
				label="group"
				v-model:value="groupModel"
				multiple
			></n-select>

			<!-- ALERT FOR WHEN USER GROUPS ARE NOT INCLUDED -->
			<br/>
			<div v-if="displayGroupPermissionIssue"
				class="alert alert-warning"
			>
				None of your user groups were included. You will not have permissions to create this object. Please
				select one of your groups
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
		isDirty: {
			type: Boolean,
			default: true,
		}, //Passes the value from the template above where the checking is done
		userGroupResults: {
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
	// computed: {
	// 	displayGroupPermissionIssue() {
	// 		const length = this.userGroupResults.filter(row => {
	// 			return this.groupModel.includes(row.group_id);
	// 		}).length;
	//
	// 		return length === 0;
	// 	},
	// },
	data() {
		return {
			groupFixResults: [],
			groupModel: [],
		};
	},
	validations: {
		groupModel: {
			required,
		},
	},
	mounted() {
		//Fix up the list to remove any django nested loops
		this.groupFixResults = this.groupResults.map((row) => {
			return {
				value: row.pk,
				label: row.fields.group_name,
			};
		});

		//Any User groups are added to the group Model
		this.groupModel = this.userGroupResults.map((row) => {
			return row.group_id;
		});
	},
};
</script>

<style scoped></style>
