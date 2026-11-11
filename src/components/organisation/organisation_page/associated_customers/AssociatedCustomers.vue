<script setup lang="ts">
import {CustomerList} from "@/components/organisation/organisation_page/associated_customers/customer_list";
import {
    email,
    maxLength,
    required, type SelectOptionInterface,
    WlkButton,
    WlkModal,
    WlkModalFooter,
    WlkModalHeader,
    WlkSelect,
    WlkTextInput
} from "whelk-ui";
import {ref} from "vue";
import {useI18n} from "petite-vue-i18n";
import {useErrorStore} from "@/stores/error/error.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {CustomerInterface} from "@/utils/interfaces/stores/CustomerInterface.ts";
import router from "@/router/router.ts";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const errorStore = useErrorStore();
const objectMetaDataStore = useObjectMetaDataStore();
const objectStore = useObjectStore();

// Define data
const fieldValidation: Record<string, boolean> = {
    emailModel: false,
    firstNamesModel: false,
    lastNameModel: false,
    titleModel: false,
};

// Define ref
const emailModel = ref<string>("");
const firstNamesModel = ref<string>("");
const isButtonDisabled = ref<boolean>(true);
const lastNamesModel = ref<string>("");
const modalClass = ref<string>("");
const titleModel = ref<string | number>("");

// Define functions
function closeModal() {
    // Close the modal
    modalClass.value = "";
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
            break;
        }
        default:
            errorStore.setError(response.statusText);
            errorStore.showErrorModal = true;
            break;
    }
}
</script>

<template>
    <div class="customers">
        <CustomerList/>

        <RouterLink
            :to="`/organisation/${objectStore.id}/customer/new/`"
        >
            <WlkButton class="compact primary create-customer"
            >
                Create Customer
            </WlkButton>
        </RouterLink>
    </div>
</template>

<style scoped>
.customers {
    > .create-customer {
        margin-top: 0.5rem;
        width: auto;
    }
}
</style>