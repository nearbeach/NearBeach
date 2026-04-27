<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref, watch, onMounted, nextTick} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			has_duplicate: "Is Duplicate Object Of",
			blocked_by: "Is Blocked By",
			blocking: "Is Currently Blocking",
			duplicate_object: "Is Duplicate Object Of",
			parent_object_of: "Is Parent Object Of",
			is_sub_object_of: "Is Sub Object Of",
			label: "Relationship",
			relates: "Relates To",
			relationship_success: "Successfully updated priority",
			relationship_updating: "Updating Priority",
		},
		ja: {
			has_duplicate: "重複オブジェクトです",
			blocked_by: "ブロックされています",
			blocking: "現在ブロック中です",
			duplicate_object: "重複オブジェクトです",
			parent_object_of: "親オブジェクトです",
			is_sub_object_of: "サブオブジェクトです",
			label: "関係",
			relates: "関連する",
			relationship_success: "優先度の更新に成功しました",
			relationship_updating: "優先度を更新中",
		},
	}
});

// Define object store
const objectStore = useObjectStore();

// Define props
const props = defineProps({
	index: {
		type: Number,
		required: true,
	},
	objectAssignmentId: {
		type: Number,
		required: true,
	},
	objectId: {
		type: Number,
		required: true,
	},
	objectType: {
		type: String,
		required: true,
	},
	relationship: {
		type: String,
		required: true,
	},
	reverseRelationship: {
		type: Boolean,
		required: true,
	},
});

// Define ref
const relationshipModel = ref<string>("");
const state = ref<string>("");

// Define constants
const relationshipList = [
	{value: "relates", label: t("relates")},
	{value: "blocked_by", label: t("blocked_by")},
	{value: "blocking", label: t("blocking")},
	{value: "sub_object_of", label: t("is_sub_object_of")},
	{value: "parent_object_of", label: t("parent_object_of")},
	{value: "has_duplicate", label: t("has_duplicate")},
	{value: "duplicate_object", label: t("duplicate_object")},
]

// Define on mounted
onMounted(() => {
	switch (props.relationship?.toLowerCase()) {
		case "block":
			relationshipModel.value = props.reverseRelationship
				? "blocked_by"
				: "blocking";
			break;
		case "duplicate":
			relationshipModel.value = props.reverseRelationship
				? "duplicate_object"
				: "duplicate_object";
			break;
		case "subobject":
			relationshipModel.value = props.reverseRelationship
				? "sub_object_of"
				: "parent_object_of";
			break;
		default:
			relationshipModel.value = "relates";
			break;
	}
});

// Define function
async function updateRelationship() {
	// Escape conditions
	if (relationshipModel.value === "") {
		return ;
	}

	// Update the state
	state.value = t("relationship_updating");

	// Save data
	fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/link_list/${props.objectAssignmentId}/`,
		{
			method: "PATCH",
			body: JSON.stringify({
				object_id: props.objectId,
				object_relation: relationshipModel.value,
				object_type: props.objectType,
			}),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	).then(() => {
		state.value = t("relationship_success");

		setTimeout(() => {
			state.value = "";
		}, 5000);
	}).catch((error) => {
		// TODO - handle errors properly
		state.value = "Error Updating";
		console.error(error);
	});
}
</script>

<template>
	<div class="relationship-link">
		<WlkSelect
			class="relationship-link compact"
			:label="t('label')"
			:options="relationshipList"
			:status="state"
			:validationRules="[required()]"
			v-model="relationshipModel"
			v-on:change="updateRelationship"
		/>
	</div>
</template>

<style scoped>
</style>
