<script setup lang="ts">
import {
	email,
	maxLength,
	required,
	WlkButton,
	WlkCard,
	WlkCardFooter,
	WlkCardHeader,
	WlkTextInput
} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";
import router from "@/router/router.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const errorStore = useErrorStore();

// Define data
const fieldValidation: Record<string, boolean> = {
	email: false,
	name: false,
	website: false,
};

// Define refs
const emailModel = ref<string>("");
const isButtonDisabled = ref<boolean>(true);
const isFormSubmitting = ref<boolean>(false);
const nameModel = ref<string>("");
const websiteModel = ref<string>("");

// Define functions
async function createOrganisation() {
	// Create body
	const body = {
		email: emailModel.value,
		name: nameModel.value,
		website: websiteModel.value,
	}

	const response = await fetch(
		`/api/v1/organisation/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		},
	);

	switch (response.status) {
		case 201: {
			// Fetch data and redirect to the new organisation
			const data: OrganisationInterface = await response.json();

			// organisation has been created
			await router.push(`/organisation/${data.id}/`);
            break;
		}
		case 403: {
			await router.push({name: "forbidden"});
            break;
		}
		default:
			errorStore.setError(response.statusText);
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

</script>

<template>
	<WlkCard class="new-organisation">
		<WlkCardHeader>
			<h1 id="main-title">{{ t(`organisation.new_organisation`) }}</h1>
			<p class="sub-text">{{ t("new_object.sub_title") }}</p>
		</WlkCardHeader>

		<div class="organisation-name">
			<WlkTextInput
				:label="t('organisation.name')"
				:validationRules="[required(), maxLength(255)]"
				v-model="nameModel"
				v-on:change="(event: { isValid: boolean }) => (updateValidation('name', event.isValid))"
			/>
		</div>

		<div class="organisation-info">
			<WlkTextInput
				:label="t('organisation.website')"
				:validationRules="[required(), maxLength(255)]"
				v-model="websiteModel"
				v-on:change="(event: { isValid: boolean }) => (updateValidation('website', event.isValid))"
			/>

			<WlkTextInput
				:label="t('organisation.email')"
				:validationRules="[required(), maxLength(255), email()]"
				v-model="emailModel"
				v-on:change="(event: { isValid: boolean }) => (updateValidation('email', event.isValid))"
			/>

		</div>

		<WlkCardFooter>
			<WlkButton
				class="primary"
				:is-action-running="isFormSubmitting"
				:disabled="isButtonDisabled"
				v-on:click="createOrganisation"
			>
				<template v-slot:default>
					{{ t("new_object.button_create") }}
				</template>

				<template v-slot:action-state>
					{{ t("new_object.button_submitting") }}
				</template>
			</WlkButton>
		</WlkCardFooter>
	</WlkCard>
</template>

<style scoped>
.new-organisation {
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

	> .organisation-info {
		display: flex;
		flex-direction: column;

		@media (--medium-screen) {
			flex-direction: row;
			justify-content: space-evenly;
		}

		> div {
			width: 100%;

			&:first-child {
				padding-right: 0.5rem;
			}

			&:last-child {
				padding-left: 0.5rem;
			}
		}
	}
}
</style>