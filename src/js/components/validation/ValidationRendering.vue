<template>
    <span
v-for="error of errorList"
		  :key="error.$uid"
		  class="error"
	>
        {{ error.$message }}
    </span>
</template>

<script>
export default {
	name: "ValidationRendering",
	props: {
		errorList: {
			type: Array,
			default: () => {
				return [];
			},
		},
	},
}
</script>
