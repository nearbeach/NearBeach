<script setup lang="ts">
import AppStructure from "@/components/structure/AppStructure.vue";
import StructureSkeleton from "@/components/structure/structure_skeleton/StructureSkeleton.vue";
import { usePermissionStore} from "@/stores/permissions/permission.ts";

// Store
const permissionStore = usePermissionStore();
</script>

<template>
	<AppStructure v-if="permissionStore.isLoaded" />
	<StructureSkeleton v-if="!permissionStore.isLoaded"/>
</template>

<style scoped>

</style>
