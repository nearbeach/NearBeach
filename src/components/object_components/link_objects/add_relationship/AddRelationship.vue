<script setup lang="ts">
import {Plus} from "@lucide/vue";
import {useI18n} from "petite-vue-i18n";
import {computed, onMounted, ref} from "vue";
import type {ObjectLinkInterface} from "@/utils/interfaces/ObjectLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			error_text: "Error fetching potential object links",
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
			error_text: "潜在的なオブジェクトリンクの取得中にエラーが発生しました",
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

// Define emit
const emit = defineEmits(["createObjectLink"])

// Define store
const objectStore = useObjectStore();

// Define models
const errorText = ref<string>("");
const relationshipModel = ref<string>("relates");
const objectSelectorModel = ref<string>("");
const objectOptions = ref<ObjectLinkInterface[]>([]);

// Define computed
const isDisabled = computed(() => {
	return objectSelectorModel.value === "";
});

// Define on mounted
onMounted(() => {
	loadData();
});

// Define functions
async function createObjectLink() {
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

async function loadData() {
	await fetch(
		"/api/v1/data/potential_object_links/",
		{
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	).then(async (response) => {
		const unfiltered_data = await response.json();

		objectOptions.value = unfiltered_data.filter((row: ObjectLinkInterface) => {
			// Base conditions
			const condition_1 = row.object_id !== objectStore.id;
			const condition_2 = row.object_type !== objectStore.destination;

			return condition_1 || condition_2;
		});
	}).catch((error) => {
		errorText.value = t("error_text") + ": " + error;
	});
}
</script>

<template>
	<div class="add-relationship">
		<div
			v-if="errorText === ''"
			class="add-relationship-label"
		>
			<label for="object-selector">{{ t("label") }}</label>
		</div>
		<div
			v-if="errorText === ''"
			class="add-relationship-object"
		>
			<select
				id="relationship-type"
				v-model="relationshipModel"
			>
				<option value="relates">{{ t("relates") }}</option>
				<option value="blocked_by">{{ t("blocked_by") }}</option>
				<option value="blocking">{{ t("blocking") }}</option>
				<option value="is_sub_object_of">{{ t("is_sub_object_of") }}</option>
				<option value="parent_object_of">{{ t("parent_object_of") }}</option>
				<option value="has_duplicate">{{ t("has_duplicate") }}</option>
				<option value="duplicate_object">{{ t("duplicate_object") }}</option>
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