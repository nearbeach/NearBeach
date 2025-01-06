<template>
	<h2>Delete Object</h2>
	<p>
		WARNING! This will delete the following {{ destination }} from the system. This can not be undone.
	</p>
	<div class="object-delete">

	</div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
	name: "DeleteObject",
	computed: {
		...mapGetters({
			destination: "getDestination",
			rootUrl: "getRootUrl",
		}),
	},
}
</script>