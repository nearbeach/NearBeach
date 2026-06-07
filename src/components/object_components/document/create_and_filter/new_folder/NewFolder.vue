<script setup lang="ts">
import {WlkButton, required, WlkTextInput, WlkModalFooter} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {computed, ref} from "vue";

// Define i18n
const {t} = useI18n({
	messages: {
		"en": {
			"cancel": "Cancel",
			"create_new_folder": "Create new folder",
			"new_folder_name": "New Folder Name",
			"new_folder_placeholder": "Statistics Folder",
		},
		"ja": {
			"cancel": "キャンセル",
			"create_new_folder": "新しいフォルダーを作成する",
			"new_folder_name": "新しいフォルダ名",
			"new_folder_placeholder": "統計フォルダ",
		}
	}
});

// Define emits
const emit = defineEmits(["closeModal"]);

// Define props
defineProps({
	currentFolderId: {
		type: Number,
		required: true,
	},
});

// Define refs
const newFolderModel = ref<string>("")

// Define computed component
const isCreateDisabled = computed(() => {
	if (newFolderModel.value === "") {
		// Disable the button
		return true;
	}
	// TODO - check the if the folder name already exists in the current folder
});

// Define functions
async function createNewFolder() {
	// TODO - connect up to the backend
	// Send the data to the backend :)
	// Update the folders in DocumentComponent
}

</script>

<template>
	<WlkTextInput class="compact"
	              :label="t('new_folder_name')"
	              :placeholderText="t('new_folder_placeholder')"
	              :validationRules="[required()]"
	              v-model="newFolderModel"
	/>
	<WlkModalFooter class="new-folder-footer">
		<WlkButton
			class="compact"
			v-on:click="emit('closeModal')"
		>
			{{t("cancel")}}
		</WlkButton>
		<WlkButton
			class="compact primary"
			:disabled="isCreateDisabled"
			v-on:click="createNewFolder"
		>
			{{t("create_new_folder")}}
		</WlkButton>
	</WlkModalFooter>
</template>

<style scoped>
.new-folder-footer {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
	padding-top: 1rem;
	margin-top: 0;
}

</style>