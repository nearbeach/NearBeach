<script setup lang="ts">
import {Plus} from "lucide-vue-next";
import {useI18n} from "petite-vue-i18n";
import {computed, ref} from "vue";

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
			label: "Add Relationship:",
			relates: "Relates To",
		},
		ja: {
			has_duplicate: "重複オブジェクトです",
			blocked_by: "ブロックされています",
			blocking: "現在ブロック中です",
			duplicate_object: "重複オブジェクトです",
			parent_object_of: "親オブジェクトです",
			is_sub_object_of: "サブオブジェクトです",
			label: "関係を追加する",
			relates: "関連する",
		},
	}
});

// Define models
const relationshipModel = ref<string>("relates");
const objectSelectorModel = ref<string>("");

// Define computed
const isDisabled = computed(() => {
	return objectSelectorModel.value === "";
});

// Define functions
async function addObjectLink() {
	// ADD CODE
}
</script>

<template>
	<div class="add-relationship">
		<div class="add-relationship-label">
			<label for="object-selector">{{t("label")}}</label>
		</div>
		<div class="add-relationship-object">
			<select
				id="relationship-type"
				v-model="relationshipModel"
			>
				<option value="relates">{{t("relates")}}</option>
				<option value="blocked_by">{{t("blocked_by")}}</option>
				<option value="blocking">{{t("blocking")}}</option>
				<option value="is_sub_object_of">{{t("is_sub_object_of")}}</option>
				<option value="parent_object_of">{{t("parent_object_of")}}</option>
				<option value="has_duplicate">{{t("has_duplicate")}}</option>
				<option value="duplicate_object">{{t("duplicate_object")}}</option>
			</select>
			<select
				id="object-selector"
				v-model="objectSelectorModel"
			>
				<option disabled selected></option>
				<option>Project 1 - Handling my pain</option>
				<option>Project 2 - Accepting the pain</option>
				<option>Task 25 - Rejecting the pain</option>
				<option>Task 26 - Where did I put my keys</option>
			</select>
			<button
				:disabled="isDisabled"
				v-on:click="addObjectLink"
			>
				<Plus />
			</button>
		</div>
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
}

</style>