<template>
	<div class="delete-object">
		<h2>Delete Object</h2>
		<p>
			WARNING! This will delete the follow {{ destination }} from the system. This can not be undone.
		</p>
		<button class="btn btn-outline-dark"
				v-on:click="confirmDeleteObject"
		>
			DELETE {{ destination }}
		</button>
	</div>

	<confirm-delete-object></confirm-delete-object>
</template>

<script>
import { mapGetters } from "vuex";
import { Modal } from "bootstrap";
import ConfirmDeleteObject from "../wizards/ConfirmDeleteObject.vue";

export default {
	name: "DeleteObject",
	components: {
		ConfirmDeleteObject
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		confirmDeleteObject() {
			const modal = new Modal(document.getElementById("confirmDeleteObjectModal"));
			modal.show();
		}
	}
}
</script>