<script setup lang="ts">
import CreateAndFilter from "@/components/object_components/document/create_and_filter/CreateAndFilter.vue";
import DocumentListRender from "@/components/object_components/document/document_list_render/DocumentListRender.vue";
import BreadCrumbs from "@/components/object_components/document/document_list_render/bread_crumbs/BreadCrumbs.vue";
</script>

<template>
	<div class="document">
		<CreateAndFilter/>
		<BreadCrumbs/>
		<DocumentListRender/>
	</div>
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