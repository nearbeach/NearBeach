<script setup lang="ts">
import {
	WlkButton,
	WlkCard,
	WlkCardHeader,
	WlkCardFooter,
	WlkTextInput,
	WlkSelect,
	required,
	maxLength,
	minLength
} from 'whelk-ui';
import {onMounted, ref, useTemplateRef} from 'vue';
import {useI18n} from "petite-vue-i18n";
import {useRoute} from "vue-router";
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import router from "@/router/router.ts";
import {failedValidation} from "@/composables/failedValidation.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define i18n
const {t} = useI18n();

// Define Route
const errorStore = useErrorStore();
const route = useRoute();

// Define Permissions
const permissionStore = usePermissionStore();

// Define data
const fieldValidation: Record<string, boolean> = {
	groupModel: false,
	titleModel: false,
};

// Define Refs
const isButtonDisabled = ref<boolean>(true);
const isFormSubmitting = ref<boolean>(false);
const groupModel = ref<string>("");
const titleModel = ref<string>("");

// Define Template Refs
const groupTemplateRef = useTemplateRef("group-ref");
const titleTemplateRef = useTemplateRef("title-ref");

// Define Functions
async function createObject(): Promise<void> {
	// Validate all the fields first
	groupTemplateRef.value?.checkValidation();
	titleTemplateRef.value?.checkValidation();
	if (failedValidation(fieldValidation)) {
		// Nothing to do
		return;
	}

	// Notify the user of the action
	isFormSubmitting.value = true;

	// Set up the form for the ajax
	const body = {
		title: titleModel.value,
		group_list: [groupModel.value],
	}

	const response = await fetch(
		`/api/v1/${route.meta.destination}/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		}
	);

	switch (response.status) {
		case 201: {
			// Get the data
			const data: { id: string } = await response.json();

			// Get the ID of the response and redirect the user to the new object
			await router.push(`/${route.meta.destination}/${data.id}`);
			break;
		}
		default:
			errorStore.setError(response);
			await router.push({name: "server-error"});
	}
}

function updateValidation(field: string, value: boolean): void {
	// Updated the field
	fieldValidation[field] = value

	// Define if everything is filled out
	isButtonDisabled.value = Object.values(fieldValidation).some((value) => {
		return !value;
	});
}

// Define on mounted
onMounted(async () => {
	// If user does not have permission - take them to the no permission page
	const permission = permissionStore.maximumPermissions[
		route.meta.destination as keyof typeof permissionStore.maximumPermissions
		] ?? 0;
	if (permission <= 1) {
		// No permission
		await router.push({name: "forbidden"});
	}
})
</script>

<template>
	<WlkCard class="new-object">
		<WlkCardHeader>
			<h1 id="main-title">{{ t(`new_object.title_${route.meta.destination}`) }}</h1>
			<p class="sub-text">{{ t("new_object.sub_title") }}</p>
		</WlkCardHeader>

		<WlkTextInput
			v-model="titleModel"
			:label="t('new_object.input_label')"
			:placeholderText="t(`new_object.placeholder_${route.meta.destination}`)"
			:validationRules="[required(), maxLength(255), minLength(5)]"
			ref="title-ref"
			v-on:change="(event: { isValid: boolean }) => (updateValidation('titleModel', event.isValid))"
		/>

		<WlkSelect
			:label="t('new_object.select_label')"
			:options="permissionStore.getUserGroups"
			:validationRules="[required()]"
			ref="group-ref"
			v-model="groupModel"
			v-on:change="(event: { isValid: boolean }) => (updateValidation('groupModel', event.isValid))"
		/>

		<WlkCardFooter>
			<WlkButton
				class="primary"
				:is-action-running="isFormSubmitting"
				:disabled="isButtonDisabled"
				v-on:click="createObject"
			>
				<template v-slot:default>
					{{ t("new_object.button_create") }}
				</template>

				<template v-slot:action-state>
					{{ t("new_object.button_submitting")}}
				</template>
			</WlkButton>
		</WlkCardFooter>
	</WlkCard>
</template>

<style scoped>
.new-object {
	border-radius: 0;
	margin: 0 auto;
	padding: 0 0.5rem;
	max-width: var(--medium-grid-width);

	@media (--medium-screen) {
		border-radius: var(--border-radius);
		padding: 0.5rem 1rem;
	}

	@media (--large-screen) {
		padding: 1rem 2rem;
	}
}
</style>
