<script setup lang="ts">
import { computed } from "vue";
import AppStructure from "@/components/structure/AppStructure.vue";
import StructureSkeleton from "@/components/structure/structure_skeleton/StructureSkeleton.vue";
import { usePermissionStore} from "@/stores/permissions/permission.ts";
import ErrorComponent from "@/components/error/ErrorComponent/ErrorComponent.vue";

// Store
const permissionStore = usePermissionStore();

// Define computed
const showStructureSkeleton = computed<boolean>(() => {
	return !permissionStore.is_loaded && !permissionStore.hasError;
});

const showErrorComponent = computed(() => {
	return !permissionStore.is_loaded && permissionStore.hasError;
})
</script>

<template>
	<AppStructure v-if="permissionStore.is_loaded" />
	<StructureSkeleton v-if="showStructureSkeleton"/>
	<ErrorComponent
		v-if="showErrorComponent"
		title="Error Fetching Permission Data"
		:message="permissionStore.getErrorInformation"
	/>
</template>

<style scoped>

</style>
