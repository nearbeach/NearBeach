<script setup lang="ts">
import ButtonComponent from '@/components/prefab/button/ButtonComponent.vue';
import CardComponent from '@/components/prefab/card/CardComponent.vue';
import CardFooter from '@/components/prefab/card/card_footer/CardFooter.vue';
import CardHeader from '@/components/prefab/card/card_header/CardHeader.vue';
import TextInput from '@/components/prefab/text_input/TextInput.vue';
import { ButtonVariantEnum } from '@/utils/enums/ButtonVariantEnum.ts';
import { ObjectStateEnum } from '@/utils/enums/ObjectStateEnum.ts';
import { nextTick, ref } from 'vue';
import router from '@/router/router.ts';

// Define Models
const titleModel = defineModel('titleModel', {
    type: String,
    default: '',
});
const groupModel = defineModel('groupModel', {
    type: String,
    default: '',
});

// Define data
const fieldValidation: Record<string, boolean> = {
    titleModel: false,
};

// Define Refs
const isFormValid = ref(true);
const objectState = ref(ObjectStateEnum.NoAction);

// Define Methods
async function createProject(): Promise<void> {
    // Check the validation
    isFormValid.value = await checkValidation();

    // Break out of save if form is not valid
    // TODO - Fix the form validation
    // if (!isFormValid.value) {
    // 	return;
    // }

    // Save the form
    objectState.value = ObjectStateEnum.Saving;

    // Wait before moving on
    setTimeout(() => {
        router.push('/project/1');
    }, 1000);
}

// Move this to utils/composition as it'll be used everywhere
async function checkValidation(): Promise<boolean> {
    // Await for a tick - make sure everything has settled
    await nextTick();

    // Loop through the field validation and find any falses
    // TODO - Fix this
    return Object.entries(fieldValidation).some((value) => {
        return !value;
    });
}
</script>

<template>
    <CardComponent class="new-project">
		<CardHeader>
			<h1 id="main-title">Create your new project</h1>
			<p class="sub-text">Fill in the details below to start your new project</p>
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
        <TextInput v-model="groupModel" label="Group Permissions" />

        <CardFooter>
            <ButtonComponent
                label="Create Project"
                :variant="ButtonVariantEnum.Primary"
                :objectState="objectState"
                v-on:click="createProject"
            />
        </CardFooter>
    </CardComponent>
</template>

<style scoped>
.new-project {
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
