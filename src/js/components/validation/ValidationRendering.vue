<template>
    <span class="error"
		  v-for="error of errorList"
		  :key="error.$uid"
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
