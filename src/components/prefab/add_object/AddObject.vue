<script setup lang="ts">
import {ObjectTitleCaseEnums} from "@/utils/enums/ObjectTitleCaseEnums.ts";

// DEFINE PROPS
const props = defineProps({
	objectType: {
		type: String,
		required: true,
		validator: function (value: string): boolean {
			const enumValues: string[] = Object.values(ObjectTitleCaseEnums);
			return enumValues.includes(value);
		},
	},
});

</script>

<template>
	<button
		class="add-object"
		type="button"
	>
		+ {{objectType}}
	</button>
</template>

<style scoped>
.add-object {
	width: 100%;
	border-style: dashed;
	border-width: var(--border-width);
	border-radius: var(--border-radius);
	padding: 0.5rem 0.75rem;
	font-weight: lighter;
	font-size: 1rem;
}



</style>