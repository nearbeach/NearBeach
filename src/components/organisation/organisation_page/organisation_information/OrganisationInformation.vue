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
import {computed, onMounted, ref} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import type {OrganisationInterface} from "@/utils/interfaces/stores/OrganisationInterface.ts";
import router from "@/router/router.ts";
import {useErrorStore} from "@/stores/error/error.ts";
import {useRoute} from "vue-router";
import {useObjectStore} from "@/stores/object/object.ts";

// Define i18n
const {t} = useI18n();

// Define router
const route = useRoute();

// Define stores
const errorStore = useErrorStore();
const objectStore = useObjectStore();

// Define data
const fieldValidation: Record<string, boolean> = {
    email: true,
    name: true,
    website: true,
};

// Define refs
const emailModel = ref<string>("");
const isButtonDisabled = ref<boolean>(true);
const nameModel = ref<string>("");
const updateState = ref<string>("loading");
const websiteModel = ref<string>("");

// Define functions
async function updateOrganisation() {
    // Notify the user of updating
    updateState.value = "updating";
    isButtonDisabled.value = true;

    // Create body
    const body = {
        email: emailModel.value,
        name: nameModel.value,
        website: websiteModel.value,
    }

    const response = await fetch(
        `/api/v1/organisation/${objectStore.id}/`,
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
        case 200:
            // Notify the user the organisation has been successfully updated
            updateState.value = "updated";

            // Set timeout to bring normal status back after 2 seconds
            setTimeout(() => {
                updateState.value = "normal";
                isButtonDisabled.value = false;
            }, 2000);

            break;
        case 403: {
            await router.push({name: "forbidden"});
            break;
        }
        default:
            errorStore.setError(response.statusText);
            await router.push({name: "server-error"});
            break;
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

// Define computed
const renderUpdateButton = computed(() => {
    switch (updateState.value) {
        case "loading":
            return t("organisation.loading");
        case "updated":
            return t("organisation.updated");
        case "updating":
            return t("organisation.updating");
        default:
            return t("organisation.update");
    }
});

// On Mounted
onMounted(async () => {
    // Clear the source
    objectStore.$reset();

    // Get the object id
    const id: string | string[] | undefined = route.params.id;
    const destination: unknown = route.meta.destination;
    if (typeof (id) !== 'string' || isNaN(parseInt(id))) {
        errorStore.setError("Invalid id");
        router.push({name: "bad-request"});
        return;
    }
    if (parseInt(id) !== parseFloat(id)) {
        errorStore.setError("Invalid id - not set as an integer");
        router.push({name: "bad-request"});
        // id is not an int
        return;
    }
    if (typeof (destination) !== 'string') {
        errorStore.setError("Invalid destination");
        router.push({name: "bad-request"});
        return;
    }

    const response = await fetch(
        `/api/v1/organisation/${id}/`,
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
            const data: OrganisationInterface = await response.json();

            // Patch
            objectStore.$patch({
                destination: "organisation",
                id: data.id,
                is_loaded: true,
            });

            // Local data
            emailModel.value = data.email;
            nameModel.value = data.name;
            websiteModel.value = data.website;

            // Set state and button
            isButtonDisabled.value = false;
            updateState.value = "normal";
            break;
        }
        case 403:
            // Use does not have access to the object
            await router.push({name: "forbidden"});
            break;
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
    <WlkCard class="new-organisation">
        <WlkCardHeader>
            <h1 id="main-title">{{ t(`organisation.title`) }}</h1>
            <p class="sub-text">{{ t("organisation.sub_title") }}</p>
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
                v-model="nameModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('email', event.isValid))"
            />

            <WlkTextInput
                :label="t('organisation.email')"
                :validationRules="[required(), maxLength(255), email()]"
                v-model="nameModel"
                v-on:change="(event: { isValid: boolean }) => (updateValidation('website', event.isValid))"
            />

        </div>

        <WlkCardFooter>
            <WlkButton
                class="primary"
                :disabled="isButtonDisabled"
                v-on:click="updateOrganisation"
            >
                {{ renderUpdateButton }}
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