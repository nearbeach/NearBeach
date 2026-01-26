<script setup lang="ts">
import {CardComponent, CardHeader, TextArea, TextInput} from 'whelk-ui';

// Define data
const fieldValidation: Record<string, boolean> = {
    descriptionModel: false,
    titleModel: false,
};

// Define Models
const titleModel = defineModel('titleModel', {
    type: String,
    default: 'Build a NearBeach project',
});
const descriptionModel = defineModel('descriptionModel', {
    type: String,
    default: '',
});
</script>

<template>
    <CardComponent class="general-details">
        <CardHeader>
            <h1 id="main-title">Project Details</h1>
			<p class="sub-text">Update and modify your project details</p>
        </CardHeader>
        <TextInput
            v-model="titleModel"
            :isRequired="true"
            :maxLength="20"
            :minLength="10"
            label="Title"
            placeholderText="Your project title"
            tooltip-title="Project Title"
            tooltip-message="Create a short title describing the project you wish to create. Minimum length of 10 characters and Maximum length of 20"
            @isValid="(value) => (fieldValidation['titleModel'] = value)"
        />
        <TextArea
            v-model="descriptionModel"
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
