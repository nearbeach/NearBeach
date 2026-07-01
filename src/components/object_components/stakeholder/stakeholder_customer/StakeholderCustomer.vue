<script setup lang="ts">

import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {ObjectTitleCaseEnums} from "whelk-ui"
import {ref} from "vue";

// Define ref
const newStakeholderModel = ref("");
</script>

<template>
	<div class="stakeholder-customer">
		<p class="stakeholder-customer-title">Customer</p>
<!--		<AddObject-->
<!--			label="Stakeholder"-->
<!--			:object-type="ObjectTitleCaseEnums.customer"-->
<!--			v-model="newStakeholderModel"-->
<!--		/>-->
	</div>
</template>

<style scoped>
.stakeholder-customer {

}

</style>