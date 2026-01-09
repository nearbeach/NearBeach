<script setup lang="ts">

import AddObject from "@/components/prefab/add_object/AddObject.vue";
import {ObjectTitleCaseEnums} from "@/utils/enums/ObjectTitleCaseEnums.ts";
</script>

<template>
	<div class="stakeholder-customer">
		<p class="stakeholder-customer-title">Customer</p>
		<AddObject
			:object-type="ObjectTitleCaseEnums.customer"
		/>
	</div>
</template>

<style scoped>
.stakeholder-customer {

}

</style>