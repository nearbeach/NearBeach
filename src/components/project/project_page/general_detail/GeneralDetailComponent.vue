<script setup lang="ts">
import {onMounted, inject} from 'vue';
import {CardComponent, CardHeader, TextArea, TextInput} from 'whelk-ui';
import type {AxiosInstance} from "axios";
import {useObjectStore} from "@/stores/object/object.ts";
import {useRoute} from "vue-router";

// Injection
const apiClient: AxiosInstance | undefined = inject("apiClient");

// Define router
const route = useRoute();

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

	// Get the project id
	const id: string | string[] | undefined = route.params.id;
	if (typeof(id) !== 'string' || isNaN(parseInt(id))) {
		// TODO - ADD ERROR HANDLING -> 400 error page
		return;
	}
	if (parseInt(id) !== parseFloat(id)) {
		// TODO - ADD ERROR HANDLING -> 400 error page
		// id is not an int
		return;
	}

	await apiClient?.get(
		`/api/v1/project/${id}/`
	).then(response => {
		objectStore.$patch(response.data);
	}).catch((error) => {
		// TODO - Handle errors -> match the error
	})

})
</script>

<template>
	<CardComponent class="general-details">
		<CardHeader>
			<h1 id="main-title">Project Details</h1>
			<p class="sub-text">Update and modify your project details</p>
		</CardHeader>
		<TextInput
			v-model="objectStore.title"
			:isRequired="true"
			:maxLength="255"
			:minLength="5"
			label="Title"
			placeholderText="Your project title"
			@isValid="(value) => (fieldValidation['titleModel'] = value)"
		/>
		<TextArea
			v-model="objectStore.description"
			placeholderText="Description of your project"
			label="Description"
			@isValid="(value) => (fieldValidation['descriptionModel'] = value)"
		/>
	</CardComponent>
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
