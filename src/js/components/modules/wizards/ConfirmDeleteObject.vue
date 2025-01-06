<template>

</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "ConfirmDeleteObject",
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			title: "getTitle",
		}),
	},
}
</script>