<script setup lang="ts">
import { WlkButton, WlkCard, WlkCardHeader, CardFooter, WlkTextInput, WlkSelect } from 'whelk-ui';
import {inject, ref} from 'vue';
import type {AxiosInstance} from "axios";
import {useI18n} from "petite-vue-i18n";
import {useRoute} from "vue-router";
import {usePermissionStore} from "@/stores/permissions/permission.ts";
import router from "@/router/router.ts";

// Injection
const apiClient = inject<AxiosInstance | undefined>("apiClient");

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			button_create: "Create",
			button_submitting: "Creating",
			input_label: "Title",
			select_label: "Select Group",
			sub_title: "Fill out the details below",
			placeholder_project: "Your project's title",
			placeholder_requirement: "Your requirement's title",
			placeholder_task: "Your task's title",
			title_project: "Create your new Project",
			title_requirement: "Create you new Requirement",
			title_task: "Create your new Task",
		},
		ja: {
			button_create: "作成する",
			button_submitting: "作成",
			input_label: "タイトル",
			select_label: "グループの選択",
			sub_title: "以下の詳細を入力してください",
			placeholder_project: "プロジェクトのタイトル",
			placeholder_requirement: "要件のタイトル",
			placeholder_task: "タスクのタイトル",
			title_project: "新しいプロジェクトを作成する",
			title_requirement: "新しい要件を作成する",
			title_task: "新しいタスクを作成する",
		},
	}
});

// Define Route
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

// Define Methods
async function createObject(): Promise<void> {
	// Notify the user of the action
	isFormSubmitting.value = true;

	// Setup the form for the ajax
	const data_to_send = new FormData();
	data_to_send.set("title", titleModel.value);
	data_to_send.set("group_list", groupModel.value);

	apiClient?.post(
		`/api/v1/${route.meta.destination}/`,
		data_to_send
	).then((response) => {
		// Get the ID of the response and redirect the user to the new object
		router.push(`/${route.meta.destination}/${response.data.id}`);
	}).catch((error) => {
		// TODO - Add in the error handling
	})
}

function updateValidation(field: string, value: boolean): void {
	console.log(field, value);
	// Updated the field
	fieldValidation[field] = value

	// Define if everything is filled out
	isButtonDisabled.value = Object.entries(fieldValidation).some(([_ , value]) => {
		return !value;
	});
}
</script>

<template>
    <WlkCard class="new-object">
		<WlkCardHeader>
			<h1 id="main-title">{{t(`title_${route.meta.destination}`)}}</h1>
			<p class="sub-text">{{t("sub_title")}}</p>
		</WlkCardHeader>

        <WlkTextInput
            v-model="titleModel"
            :isRequired="true"
			:label="t('input_label')"
			:placeholderText="t(`placeholder_${route.meta.destination}`)"
            :maxLength="255"
            :minLength="5"
            @isValid="(value) => (updateValidation('titleModel', value))"
        />

		<WlkSelect
			:is-required="true"
			:label="t('select_label')"
			:options="permissionStore.getUserGroups"
			v-model="groupModel"
			@isValid="(value) => (updateValidation('groupModel', value))"
		/>

        <CardFooter>
            <WlkButton
				class="primary"
				:is-action-running="isFormSubmitting"
				:is-disabled="isButtonDisabled"
                v-on:click="createObject"
			>
				{{t("button_create")}}
			</WlkButton>
        </CardFooter>
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
