<script setup lang="ts">
import {useObjectStore} from "@/stores/object/object.ts";
import ProfilePicture from "@/components/prefab/profile_picture/ProfilePicture.vue";
import {useI18n} from "petite-vue-i18n";
import {onMounted, ref, watch} from "vue";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import {WlkRenderErrorMessage} from "whelk-ui";
import type {ResponseInterface} from "@/utils/interfaces/ResponseInterface.ts";

// Define i18n
const {t} = useI18n();

// Define Stores
const objectStore = useObjectStore();

// Define refs
const errorMessage = ref<string>("");

// Define Watches
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value && objectStore.customers.length === 0) {
			await fetchCustomerList();
		}
	}
)

// Define functions
async function fetchCustomerList() {
    // Fetch customer data
    const response = await fetch(
        `/api/v1/organisation/${objectStore.id}/customer/`,
        {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFTOKEN": getCsrfToken(),
            },
        }
    );

    switch (response.status) {
        case 200: {
            // Get
            const data: ResponseInterface = await response.json();

            // Patch
            objectStore.$patch({
                customers: data.results ?? [],
            });
            break;
        }
        default:
            errorMessage.value = response.statusText;
            break;
    }
}

// On Mounted
onMounted(async () => {
    if (objectStore.is_loaded) {
        // Load the data
        await fetchCustomerList();
    }
});
</script>

<template>
    <div class="customer-list"
         v-if="objectStore.customers.length > 0"
    >
        <div class="customer-item"
             v-for="(customer) in objectStore.customers"
             :key="customer.id"
        >
                <ProfilePicture :url="customer.profile_picture" :name="customer.first_name" />
				<div class="details">
					<div class="name">
                        <RouterLink :to="`/organisation/${objectStore.id}/customer/${customer.id}/`">
						    {{ customer.title.title ?? "" }} {{ customer.first_name }} {{ customer.last_name }}
                        </RouterLink>
					</div>
                    <div class="email">
						<strong>{{t("customer.email")}}: </strong>{{customer.email}}
                    </div>
				</div>
        </div>
        <WlkRenderErrorMessage v-if="errorMessage !== ''">{{errorMessage}}</WlkRenderErrorMessage>
    </div>
    <div v-else
         class="empty-customer-list"
    >
        {{ t("customer.empty_customer_list") }}
    </div>
</template>

<style scoped>
.customer-list {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 1.5rem;
    border-bottom: 1px dashed;

    @media (--medium-screen) {
        flex-direction: row;
        justify-content: space-between;
    }

    .customer-item {
        width: 100%;
        border: 1px dotted;
        padding: 1rem;
        margin: 0 0 0.75rem 0;

        @media (--medium-screen) {
            width: 45%;
        }
    }
}

.empty-customer-list {
	margin-top: 2rem;
	height: 7rem;
	display: flex;
	justify-content: center;
	align-items: center;
	font-size: 1.25rem;
	font-weight: 100;
	font-family: "Roboto", sans-serif;
	border: dashed;
	border-radius: var(--border-radius);
	border-width: var(--border-width);
}
</style>