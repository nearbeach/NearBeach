<script setup lang="ts">
import {CustomerList} from "@/components/organisation/organisation_page/associated_customers/customer_list";
import {WlkButton} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {useObjectStore} from "@/stores/object/object.ts";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n();

// Define stores
const objectStore = useObjectStore();
const permissionStore = usePermissionStore();

</script>

<template>
    <div class="customers">
        <CustomerList/>

        <RouterLink :to="`/organisation/${objectStore.id}/customer/new/`">
            <WlkButton v-if="permissionStore.currentObjectPermissions.currentObject > 1"
					   class="compact primary create-customer"
			>
                {{t("customer.create")}}
            </WlkButton>
        </RouterLink>
    </div>
</template>

<style scoped>
.customers {
    .empty-customer-list {
        margin-bottom: 0.5rem;
    }
}
</style>