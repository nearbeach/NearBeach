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
import {onMounted, ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {useErrorStore} from "@/stores/error/error.ts";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";
import router from "@/router/router.ts";

// Define i18n
const {t} = useI18n();

// Define props
const props = defineProps({
    customerId: {
        type: String,
        required: true,
    },
    // The organisation id
    id: {
        type: String,
        required: true,
    },
})

// Define stores
const errorStore = useErrorStore();
const objectMetaDataStore = useObjectMetaDataStore();

// Define data
const fieldValidation: Record<string, boolean> = {
    email: true,
    first_name: true,
    last_name: true,
    title: true,
};

// Define refs
const emailModel = ref<string>("");
const firstNamesModel = ref<string>("");
const isUpdateButtonDisabled = ref<boolean>(true);
const lastNamesModel = ref<string>("");
const renderUpdateButton = ref<string>(t("customer.loading"));
const titleModel = ref<string | number>("");

// Define functions
async function updateCustomer() {
    // Update button
    isUpdateButtonDisabled.value = true;
    renderUpdateButton.value = t("customer.updating");

    // Create body
    const body = {
        title: titleModel.value,
        first_name: firstNamesModel.value,
        last_name: lastNamesModel.value,
        email: emailModel.value,
    }

    const response = await fetch(
        `/api/v1/organisation/${props.id}/customer/${props.customerId}/`,
        {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": getCsrfToken(),
            },
            body: JSON.stringify(body),
        },
    );

    switch (response.status) {
        case 200: {
            renderUpdateButton.value = t("customer.updated");

            setTimeout(() => {
                renderUpdateButton.value = t("customer.update");
                isUpdateButtonDisabled.value = false;
            }, 2000);
            break;
        }
        default:
            errorStore.setError(response.statusText);
            errorStore.showErrorModal = true;
            break;
    }
}

function updateValidation(field: string, value: boolean): void {
    // Updated the field
    fieldValidation[field] = value

    // Define if everything is filled out
    isUpdateButtonDisabled.value = Object.values(fieldValidation).some((value) => {
        return !value;
    });
}

// On Mounted
onMounted(async () => {
    // Fetch the data
    const response = await fetch(
        `/api/v1/organisation/${props.id}/customer/${props.customerId}/`,
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
            const data : CustomerInterface = await response.json();

            // Set data
            emailModel.value = data.email;
            firstNamesModel.value = data.first_name;
            lastNamesModel.value = data.last_name;
            titleModel.value = data.title.id;

            // Update buttons state
            isUpdateButtonDisabled.value = false;
            renderUpdateButton.value = t("customer.update");

            break;
        }
        case 404:
            // Object does not exist
            await router.push({name: "not-found"});
            break;
        default:
            // Assuming a 500 error
            errorStore.setError(response);
            await router.push({name: "server-error"});
            break;
    }
})
</script>

<template>
    <WlkCard class="customer">
        <WlkCardHeader>
            <h1 id="main-title">{{ t(`customer.title`) }}</h1>
            <p class="sub-text">{{ t("customer.sub_text") }}</p>
        </WlkCardHeader>

        <div class="customer-name">
            <WlkSelect
                optionsLabel="title"
                optionsValue="id"
                :label="t('customer.title')"
                :options="objectMetaDataStore.customer_titles"
                :validationRules="[required()]"
                v-model="titleModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('title', event.isValid))"
            />
            <WlkTextInput
                :label="t('customer.first_name')"
                :validationRules="[required(), maxLength(255)]"
                v-model="firstNamesModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('first_name', event.isValid))"
            />
            <WlkTextInput
                :label="t('customer.last_name')"
                :validationRules="[required(), maxLength(255)]"
                v-model="lastNamesModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('last_name', event.isValid))"
            />
        </div>

        <div class="customer-email">
            <WlkTextInput
                :label="t('customer.email')"
                :validationRules="[required(), maxLength(255), email()]"
                v-model="emailModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('email', event.isValid))"
            />
        </div>

        <WlkCardFooter class="customer-footer">
            <RouterLink :to="`/organisation/${props.id}/`">
                <WlkButton>
                    {{t("customer.back_to_org")}}
                </WlkButton>

            </RouterLink>
            <WlkButton
                class="primary"
                :disabled="isUpdateButtonDisabled"
                v-on:click="updateCustomer"
            >
                {{ renderUpdateButton }}
            </WlkButton>
        </WlkCardFooter>
    </WlkCard>
</template>

<style scoped>
.customer {
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

    > .customer-name {
        display: flex;
        flex-direction: column;

        @media (--medium-screen) {
            flex-direction: row;
            justify-content: space-between;

            > div:first-child {
                width: 100px;
            }
        }
    }

    > .customer-footer {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
}
</style>
