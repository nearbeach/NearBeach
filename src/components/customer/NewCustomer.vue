<script setup lang="ts">
import {
    email,
    maxLength,
    required,
    WlkButton,
    WlkCard,
    WlkCardFooter,
    WlkCardHeader,
    WlkSelect,
    WlkTextInput
} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {ref} from "vue";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface";
import router from "@/router/router.ts";
import {useErrorStore} from "@/stores/error/error.ts";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const errorStore = useErrorStore();
const objectStore = useObjectStore();
const permissionStore = usePermissionStore();

// Define data
const fieldValidation: Record<string, boolean> = {
    emailModel: false,
    firstNamesModel: false,
    lastNameModel: false,
    titleModel: false,
};

// Define refs
const emailModel = ref<string>("");
const firstNamesModel = ref<string>("");
const isButtonDisabled = ref<boolean>(true);
const isFormSubmitting = ref<boolean>(false);
const lastNamesModel = ref<string>("");
const titleModel = ref<string | number>("");

// Define functions
async function cancel() {
    // Go back to organisation
    await router.push(`/organisation/${objectStore.id}/`);
}

async function createCustomer() {
    // Create body
    const body = {
        title: titleModel.value,
        first_names: firstNamesModel.value,
        last_names: lastNamesModel.value,
        email: emailModel.value,
    }

    const response = await fetch(
        `/api/v1/organisation/${objectStore.id}/customer/`,
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
            // Fetch data and redirect to the new customer
            const data: CustomerInterface = await response.json();

            // Customer has been created
            await router.push(`/organisation/${objectStore.id}/customer/${data.id}/`);
        }
        case 403: {
            await router.push({name: "forbidden"});
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
    <WlkCard class="new-customer">
        <WlkCardHeader>
            <h1 id="main-title">{{ t(`new_object.title_customer`) }}</h1>
            <p class="sub-text">{{ t("new_object.sub_title") }}</p>
        </WlkCardHeader>

        <div class="customer-name">
            <WlkSelect
                :label="t('new_object.select_customer_title')"
                :options="permissionStore.customerTitles"
                :validationRules="[required()]"
                v-model="titleModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('title', event.isValid))"
            />
            <WlkTextInput
                :label="t('new_object.customer_first_name')"
                :validationRules="[required(), maxLength(255)]"
                v-model="firstNamesModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('first_name', event.isValid))"
            />
            <WlkTextInput
                :label="t('new_object.customer_last_name')"
                :validationRules="[required(), maxLength(255)]"
                v-model="lastNamesModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('last_name', event.isValid))"
            />
        </div>

        <div class="customer-email">
            <WlkTextInput
                :label="t('new_object.customer_email')"
                :validationRules="[required(), maxLength(255), email()]"
                v-model="emailModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('email', event.isValid))"
            />
        </div>

        <WlkCardFooter>
            <RouterLink
                :to="`/organisation/${objectStore.id}/`"
            >
                <WlkButton
                    class="danger"
                    v-on:click="cancel"
                >
                    {{ t("customer.cancel") }}
                </WlkButton>
            </RouterLink>
            <WlkButton
                class="primary"
                :is-action-running="isFormSubmitting"
                :disabled="isButtonDisabled"
                v-on:click="createCustomer"
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
.new-customer {
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