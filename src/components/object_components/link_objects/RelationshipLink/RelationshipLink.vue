<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref, watch, onMounted} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			has_duplicate_object_of: "Is Duplicate Object Of",
			is_blocked_by: "Is Blocked By",
			is_currently_blocking: "Is Currently Blocking",
			is_duplicate_object_of: "Is Duplicate Object Of",
			is_parent_object_of: "Is Parent Object Of",
			is_sub_object_of: "Is Sub Object Of",
			label: "Relationship",
			relates_to: "Relates To",
			relationship_success: "Successfully updated priority",
			relationship_updating: "Updating Priority",
		},
		ja: {
			has_duplicate_object_of: "重複オブジェクトです",
			is_blocked_by: "ブロックされています",
			is_currently_blocking: "現在ブロック中です",
			is_duplicate_object_of: "重複オブジェクトです",
			is_parent_object_of: "親オブジェクトです",
			is_sub_object_of: "サブオブジェクトです",
			label: "関係",
			relates_to: "関連する",
			relationship_success: "優先度の更新に成功しました",
			relationship_updating: "優先度を更新中",
		},
	}
});

// Define props
const props = defineProps({
	index: {
		type: Number,
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
	{value: "relates_to", label: t("relates_to")},
	{value: "is_blocked_by", label: t("is_blocked_by")},
	{value: "is_currently_blocking", label: t("is_currently_blocking")},
	{value: "is_sub_object_of", label: t("is_sub_object_of")},
	{value: "is_parent_object_of", label: t("is_parent_object_of")},
	{value: "has_duplicate_object_of", label: t("has_duplicate_object_of")},
	{value: "is_duplicate_object_of", label: t("is_duplicate_object_of")},
]

// Define store

// Define watchers
watch(relationshipModel, (new_value, old_value) => {
	// If new value the same in the state - do nothing
	if (new_value === old_value) {
		return;
	}

	state.value = t("relationship_updating");

	// Fetch the status
	const priority = relationshipList[parseInt(new_value)];
	if (priority === undefined) {
		// We have an issue
		// TODO - Do propper error handling
		console.error(`Status was not found in state management: ${new_value}`)
		state.value = "Error Updating";
		return;
	}

	// Save data
	/*
	fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/`,
		{
			method: "PATCH",
			body: JSON.stringify({
				priority: new_value,
			}),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	).then(() => {
		state.value = t("priority_success");

		setTimeout(() => {
			state.value = "";
		}, 5000);
	}).catch((error) => {
		// TODO - handle errors properly
		state.value = "Error Updating";
		console.error(error);
	});
	*/
});

onMounted(() => {
	switch (props.relationship?.toLowerCase()) {
		case "block":
			relationshipModel.value = props.reverseRelationship
				? "is_blocked_by"
				: "is_currently_blocking";
			break;
		case "duplicate":
			relationshipModel.value = props.reverseRelationship
				? "has_duplicate_object_of"
				: "is_duplicate_object_of";
			break;
		case "subobject":
			relationshipModel.value = props.reverseRelationship
				? "is_sub_object_of"
				: "is_parent_object_of";
			break;
		default:
			relationshipModel.value = "relates_to";
			break;
	}
});
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
		/>
	</div>
</template>

<style scoped>
</style>
