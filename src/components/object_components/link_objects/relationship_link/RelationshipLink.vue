<script setup lang="ts">
import {required, WlkSelect} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref, onMounted} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useObjectStore} from "@/stores/object/object.ts";

// Define i18n
const {t} = useI18n();

// Define the emits
const emit = defineEmits(["updateRelationship"]);

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
	{value: "relates", label: t("relationship_link.relates")},
	{value: "blocked_by", label: t("relationship_link.blocked_by")},
	{value: "blocking", label: t("relationship_link.blocking")},
	{value: "sub_object_of", label: t("relationship_link.is_sub_object_of")},
	{value: "parent_object_of", label: t("relationship_link.parent_object_of")},
	{value: "has_duplicate", label: t("relationship_link.has_duplicate")},
	{value: "duplicate_object", label: t("relationship_link.duplicate_object")},
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
function updateRelationship() : void {
	// Escape conditions
	if (relationshipModel.value === "") {
		return;
	}

	if (props.index < 0) {
		return;
	}


	// Update the state
	state.value = t("relationship_link.relationship_updating");

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
		state.value = t("relationship_link.relationship_success");
		emit("updateRelationship", { index: props.index, link_relationship: relationshipModel.value});

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
			:label="t('relationship_link.label')"
			:options="relationshipList"
			:status="state"
			:validationRules="[required()]"
			v-model="relationshipModel"
			v-on:change="updateRelationship"
		/>
	</div>
</template>
