<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import {required, WlkButton, WlkModalFooter} from "whelk-ui";
import {computed, ref} from "vue";

// Define i18n
const {t} = useI18n({
	messages: {
		"en": {
			"description": "Description",
			"url": "Url Location",
		},
		"ja": {
			"description": "説明",
			"url": "URLの場所",
		},
	}
});

// Define emits
const emit = defineEmits(["closeModal"]);

// Define refs
const descriptionModel = ref("");
const newLinkModel = ref("");

// Define computed
const isCreateDisabled = computed(() => {
	return newLinkModel.value === "";
})

// Define function
async function createNewLink() {
	// TODO - Create new link and pass information up
}

</script>

<template>
	<WlkTextInput class="compact"
				  placeholder="https://nearbeach.org/"
				  :label="t('url')"
				  :validationRules="[required()]"
				  v-model="newLinkModel"
	/>
	<WlkTextInput class="compact"
				  :label="t('description')"
				  v-model="descriptionModel"
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
			v-on:click="createNewLink"
		>
			{{t("create_new_folder")}}
		</WlkButton>
	</WlkModalFooter>
</template>

<style scoped>

</style>