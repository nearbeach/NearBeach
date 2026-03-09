<script setup lang="ts">
import { CardComponent, CardHeader } from "whelk-ui"
import CreateAndFilter from "@/components/project/project_page/document/create_and_filter/CreateAndFilter.vue";
import DocumentListRender from "@/components/project/project_page/document/document_list_render/DocumentListRender.vue";
import BreadCrumbs from "@/components/project/project_page/document/document_list_render/bread_crumbs/BreadCrumbs.vue";

</script>

<template>
	<CardComponent class="document-component">
		<CardHeader>
			<h2>Project Documentation</h2>
		</CardHeader>
		<CreateAndFilter />
		<BreadCrumbs />
		<DocumentListRender />
	</CardComponent>
</template>

<style scoped>
.document-component {
	padding: 0 0.5rem;

	@media (--medium-screen) {
		padding: 0.5rem;
	}

	@media (--large-screen) {
		padding: 0.5rem 1rem;
	}
}
</style>