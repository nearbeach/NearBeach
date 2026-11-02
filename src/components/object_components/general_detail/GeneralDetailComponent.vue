<script setup lang="ts">
import {onMounted, ref, computed} from 'vue';
import {maxLength, minLength, required, WlkButton, WlkCard, WlkCardHeader, WlkTextArea, WlkTextInput} from 'whelk-ui';
import {useObjectStore} from "@/stores/object/object.ts";
import {useRoute} from "vue-router";
import {useI18n} from "petite-vue-i18n";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import router from "@/router/router.ts";
import {useErrorStore} from "@/stores/error/error.ts";

// Define i18n
const {t} = useI18n()

// Define router
const errorStore = useErrorStore();
const route = useRoute();

// Define refs
const updateState = ref("normal");

// Define stores
const objectStore = useObjectStore();

// Define data
const fieldValidation: Record<string, boolean> = {
	descriptionModel: false,
	titleModel: false,
};

// Define onMount
onMounted(async () => {
	// Clear the source
	objectStore.$reset();

	// Get the object id
	const id: string | string[] | undefined = route.params.id;
	const destination: unknown = route.meta.destination;
	if (typeof (id) !== 'string' || isNaN(parseInt(id))) {
		// TODO - ADD ERROR HANDLING -> 400 error page
		return;
	}
	if (parseInt(id) !== parseFloat(id)) {
		// TODO - ADD ERROR HANDLING -> 400 error page
		// id is not an int
		return;
	}
	if (typeof (destination) !== 'string') {
		// TODO - ADD ERROR HANDLING -> 400 error page
		return;
	}

	try {

		const response = await fetch(
			`/api/v1/${destination}/${id}/`,
			{
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				}
			}
		);

		switch (response.status) {
			case 200: {
				// Get data
				const data = await response.json();
				data.destination = destination;
				data.is_loaded = true;

				// Patch
				objectStore.$patch(data);
				break;
			}
			case 403:
				// Use does not have access to the object
				return router.push({name: "forbidden"});
			case 404:
				// Object does not exist
				return router.push({name: "not-found"});
			default:
				// Assuming a 500 error
				errorStore.setError(response);
				return router.push({name: "server-error"});
		}
	} catch (error) {
		// Assuming a 500 error
		errorStore.setError(error);
		return router.push({name: "server-error"});
	}
	
	return null;
});

// Define computed
const isUpdateButtonDisabled = computed(() => {
	return updateState.value !== "normal";
});

const renderUpdateButton = computed(() => {
	switch (updateState.value) {
		case "error":
			return t("general_detail_component.update_error");
		case "updated":
			return t("general_detail_component.updated");
		case "updating":
			return t("general_detail_component.updating");
		default:
			return t("general_detail_component.update");
	}
});

// Define functions
function updateData() {
	// Notify the user of the state change
	updateState.value = "updating"

	fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/`,
		{
			method: "PATCH",
			body: JSON.stringify({
				title: objectStore.title,
				description: objectStore.description,
			}),
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			}
		}
	).then(() => {
		updateState.value = "updated";

		setTimeout(() => {
			updateState.value = "normal";
		}, 2000);
	}).catch((error) => {
		// TODO - handle errors property
		updateState.value = "error";

		console.error("ERROR: ", error);

		// setTimeout(() => {
		// 	updateState.value = "normal";
		// })
	});
}
</script>

<template>
	<WlkCard class="general-details">
		<WlkCardHeader>
			<h1 id="main-title">{{ t(`general_detail_component.${objectStore.destination}_details`) }}</h1>
			<p class="sub-text">{{ t(`general_detail_component.${objectStore.destination}_sub_text`) }}</p>
		</WlkCardHeader>
		<WlkTextInput
			v-model="objectStore.title"
			:label="t('general_detail_component.title')"
			:validationRules="[required(), maxLength(255), minLength(5)]"
			:placeholderText="t(`general_detail_component.${objectStore.destination}_title_placeholder`)"
			v-on:change="(event: { isValid: boolean }) => (fieldValidation['titleModel'] = event.isValid)"
		/>
		<WlkTextArea
			v-model="objectStore.description"
			:label="t('general_detail_component.description')"
			:placeholderText="t(`general_detail_component.${objectStore.destination}_description_placeholder`)"
		/>

		<WlkButton
			class="primary"
			:disabled="isUpdateButtonDisabled"
			v-on:click="updateData"
		>
			{{ renderUpdateButton }}
		</WlkButton>
	</WlkCard>

</template>

<style scoped>
.general-details {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem 1rem;
	}

	@media (--large-screen) {
		padding: 0.5rem 1rem;
	}
}
</style>
