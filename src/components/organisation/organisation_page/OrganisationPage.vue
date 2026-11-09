<script setup lang="ts">
import {GeneralDetailComponent} from '@/components/object_components/general_detail';
import {PropertiesComponent} from '@/components/object_components/properties_component';
import {AccessComponent} from "@/components/object_components/access";
import {PublicLinks} from "@/components/object_components/public_links";
import {StakeholderComponent} from "@/components/object_components/stakeholder";
import {DocumentComponent} from "@/components/object_components/document";
import {NotesComponent} from "@/components/object_components/notes";
import {LinkObjects} from "@/components/object_components/link_objects";
import {SprintLinks} from "@/components/object_components/sprint_links";
import type {TabHeaderInterface} from "whelk-ui";
import {WlkCard, WlkTabs} from "whelk-ui";
import {onMounted} from "vue";
import {useObjectMetaDataStore} from "@/stores/object_meta_data/object_meta_data.ts";
import {useI18n} from "petite-vue-i18n";

// Define i18n
const {t} = useI18n()

// Define variables
const tabList: TabHeaderInterface[] = [
	{label: t("organisation_page.contacts"), for: "contacts"},
	{label: t("organisation_page.documentation"), for: "documentation"},
	{label: t("organisation_page.associated_objects"), for: "associated_objects"},
	{label: t("organisation_page.notes"), for: "notes"},
	{label: t("organisation_page.misc"), for: "misc"},
]

// Define stores
const objectMetaDataStore = useObjectMetaDataStore();

onMounted(() => {
	objectMetaDataStore.updateObjectStatus("organisation");
});
</script>

<template>
	<div class="organisation-information">
		<div class="container">

			<WlkCard class="extra-information">
				<WlkTabs :tabList="tabList">
					<template #link_objects>
						<LinkObjects/>
					</template>
					<template #documentation>
						<DocumentComponent/>
					</template>
					<template #notes>
						<NotesComponent/>
					</template>
					<template #misc>
						<PublicLinks/>
                        <hr />
                        <SprintLinks />
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
