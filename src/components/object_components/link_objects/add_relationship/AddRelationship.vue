<script setup lang="ts">
import {Plus} from "@lucide/vue";
import {useI18n} from "petite-vue-i18n";
import {computed, type PropType, ref} from "vue";
import type {ObjectLinkInterface} from "@/utils/interfaces/ObjectLinkInterface.ts";

// Define i18n
const {t} = useI18n();

// Define emit
const emit = defineEmits(["createObjectLink"])

// Define props
defineProps({
    objectOptions: {
        type: Array as PropType<ObjectLinkInterface[]>,
        required: true,
    },
})

// Define models
const errorText = ref<string>("");
const relationshipModel = ref<string>("relates");
const objectSelectorModel = ref<string>("");

// Define computed
const isDisabled = computed(() => {
	return objectSelectorModel.value === "";
});

// Define functions
function createObjectLink() : void {
	// Escape conditions
	if (objectSelectorModel.value === null || objectSelectorModel.value === "") {
		// Nothing to do
		return;
	}

	// Emit upstream
	emit("createObjectLink", {
		"objectSelectorModel": objectSelectorModel.value,
		"relationshipModel": relationshipModel.value
	});
}
</script>

<template>
	<div class="add-relationship">
		<div
			v-if="errorText === ''"
			class="add-relationship-label"
		>
			<label for="object-selector">{{ t("add_relationship.label") }}</label>
		</div>
		<div
			v-if="errorText === ''"
			class="add-relationship-object"
		>
			<select
				id="relationship-type"
				v-model="relationshipModel"
			>
				<option value="relates">{{ t("add_relationship.relates") }}</option>
				<option value="blocked_by">{{ t("add_relationship.blocked_by") }}</option>
				<option value="blocking">{{ t("add_relationship.blocking") }}</option>
				<option value="is_sub_object_of">{{ t("add_relationship.is_sub_object_of") }}</option>
				<option value="parent_object_of">{{ t("add_relationship.parent_object_of") }}</option>
				<option value="has_duplicate">{{ t("add_relationship.has_duplicate") }}</option>
				<option value="duplicate_object">{{ t("add_relationship.duplicate_object") }}</option>
			</select>
			<select
				id="object-selector"
				v-model="objectSelectorModel"
			>
				<option disabled selected></option>
				<option v-for="object in objectOptions"
				        :key="object.object_id"
				        :value="`${object.object_type}-${object.object_id}`"
				>
					{{ object.object_type }}{{ object.object_id }} - {{ object.object_title }}
				</option>
			</select>
			<button
				:disabled="isDisabled"
				v-on:click="createObjectLink"
			>
				<Plus/>
			</button>
		</div>

		<div
			v-if="errorText !== ''"
			class="error"
		>{{ errorText }}</div>
	</div>
</template>

<style scoped>
.add-relationship {
	display: flex;
	flex-direction: column;
	margin-bottom: 1.25rem;

	> .add-relationship-label > label {
		font-size: 0.75rem;
		font-weight: bold;
	}

	> .add-relationship-object {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;

		> select {
			font-size: 0.75rem;
			font-weight: lighter;
		}

		> #relationship-type {
			border: 1px dashed black;
			border-radius: 0.25rem 0 0 0.25rem;
		}

		> #object-selector {
			border-top: 1px dashed black;
			border-right: none;
			border-bottom: 1px dashed black;
			border-left: none;
			width: 100%;
		}

		> button {
			border: 1px dashed black;
			border-radius: 0 0.25rem 0.25rem 0;
			display: flex;
			background-color: var(--secondary);

			> svg {
				width: 1rem;
				height: 1rem;
			}

			&:hover {
				background-color: var(--secondary-hover);
			}

			&:disabled {
				background-color: var(--border-muted);
			}
		}
	}

	> .error {
		color: var(--danger);
	}
}

</style>