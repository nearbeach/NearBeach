<script setup lang="ts">
import GeneralDetailComponent from '@/components/project/project_page/general_detail/GeneralDetailComponent.vue';
import PropertiesComponent from '@/components/project/project_page/properties_component/PropertiesComponent.vue';
import AccessComponent from "@/components/project/project_page/access/AccessComponent.vue";
import PublicLinks from "@/components/project/project_page/public_links/PublicLinks.vue";
import StakeholderComponent from "@/components/project/project_page/stakeholder/StakeholderComponent.vue";
import DocumentComponent from "@/components/project/project_page/document/DocumentComponent.vue";
import NotesComponent from "@/components/project/project_page/notes/NotesComponent.vue";
import LinkObjects from "@/components/project/project_page/LinkObjects/LinkObjects.vue";
import SprintPlanning from "@/components/project/project_page/sprint/SprintPlanning.vue";
</script>

<template>
    <div class="project-information">
		<div class="container">
			<GeneralDetailComponent />
			<PropertiesComponent />
			<LinkObjects />
			<DocumentComponent />
			<NotesComponent />
		</div>
		<div class="properties">
			<PropertiesComponent />
			<AccessComponent />
			<StakeholderComponent />
			<PublicLinks />
			<SprintPlanning />
		</div>
    </div>
</template>

<style scoped>
.project-information {
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

		> .card {
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
