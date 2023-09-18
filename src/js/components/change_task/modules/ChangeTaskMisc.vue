<template>
	<is-downtime></is-downtime>

	<hr/>
	<required-by></required-by>
</template>

<script>
import IsDowntime from './IsDowntime.vue'
import RequiredBy from './RequiredBy.vue'

export default {
	name: "ChangeTaskMisc",
	components: {
		IsDowntime,
		RequiredBy,
	},
}
</script>