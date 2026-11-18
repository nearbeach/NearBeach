<script setup lang="ts">
import {type TabHeaderInterface, WlkCard, WlkTabs} from "whelk-ui";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {onMounted} from "vue";
import {CustomerInformation} from "@/components/customer/customer_page/customer_infomration";
import {useI18n} from "petite-vue-i18n";
import {AssociatedObjects} from "@/components/organisation/organisation_page/associated_objects";

// Define i18n
const {t} = useI18n()

// Define variables
const tabList: TabHeaderInterface[] = [
	{label: t("customer.associated_objects"), for: "associated_objects"},
]

// Define props
defineProps({
    customerId: {
        type: String,
        required: true,
    },
    // The organisation id
    id: {
        type: String,
        required: true,
    },
});

// Define stores
const objectMetaDataStore = useObjectMetaDataStore();

onMounted(() => {
	objectMetaDataStore.updateObjectStatus("customer");
});
</script>

<template>
	<div class="organisation-information">
		<div class="container">
			<CustomerInformation :customer-id="customerId"
								 :id="id"
			/>

			<WlkCard class="extra-information">
				<WlkTabs :tabList="tabList">
                    <template #associated_objects>
                        <AssociatedObjects />
                    </template>
				</WlkTabs>
			</WlkCard>
		</div>
	</div>
</template>

<!--suppress CssUnusedSymbol -->
<style scoped>
.organisation-information {
	max-width: calc(var(--x-large-card-width));
	display: flex;
	justify-content: center;
	flex-direction: column;

	@media (--medium-screen) {
		margin: 0 0.5rem;
	}

	@media (--large-screen) {
		flex-direction: row;
	}

	> .container {
		@media (--large-screen) {
			width: 100%;
			max-width: var(--large-grid-width);
			margin-right: 0.25rem;
		}

		> .properties-component {
			@media (--large-screen) {
				display: none;
			}
		}

		> .extra-information {
			> div {
				padding: 0 0.5rem;

				@media (--medium-screen) {
					padding: 0.5rem 1rem;
				}

				@media (--large-screen) {
					padding: 0.5rem 1rem;
				}
			}
		}

		> .wlk-card, .wlk-card-component {
			margin-bottom: 1rem;
		}
	}

	> .properties {
		@media (--large-screen) {
			width: 320px;
			min-width: 320px;
			max-width: 320px;
			margin-left: 0.25rem;
		}

		> .properties-component {
			display: none;

			@media (--large-screen) {
				display: block;
			}
		}

		> .card {
			margin-bottom: 1rem;

			@media (--large-screen) {
				margin-bottom: 0.5rem;
			}
		}
	}
}
</style>
