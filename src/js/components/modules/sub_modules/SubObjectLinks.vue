<template>
	<h3 v-if="linkResults.length > 0">
		{{ title }}
	</h3>
	<div v-for="link in linkResults"
		 v-bind:key="link.pk"
		 class="row object-link"
	>
		<!-- Object ID + Title -->
		<div class="col-md-10 object-link--details">
			<a v-bind:href="`${this.rootUrl}${link.object_type}_information/${link.object_id}/`"
			   target="_blank"
			   rel="noopener noreferrer"
			>
				<div class="object-link--link">{{ link.object_type }} - {{ link.object_id }}</div>
				<div class="object-link--title">{{ link.object_title }}</div>
			</a>
		</div>

		<!-- Object Status -->
		<div class="col-md-2 object-link--status">
			<span>Object Status: </span>
			<span>
                {{ link.object_status }}
            </span>
		</div>

		<!-- Object Delete -->
		<div
			class="object-link--remove"
			v-if="userLevel >= 2 && canDelete === true"
		>
			<carbon-trash-can
				v-on:click="confirmRemoveLink(link)"
			></carbon-trash-can>
		</div>
	</div>
	<div class="spacer-extra"
		 v-if="linkResults.length > 0"
	></div>
</template>

<script>
import {mapGetters} from "vuex";

import {Modal} from "bootstrap";
import {CarbonTrashCan} from "../../../components";

export default {
	name: "SubObjectLinks",
	components: {
		CarbonTrashCan,
	},
	emits: ["update_link_results"],
	props: {
		canDelete: {
			type: Boolean,
			default: true,
		},
		linkResults: {
			type: Array,
			default: () => {
				return [];
			},
		},
		title: {
			type: String,
			default: "Relates",
		},
	},
	computed: {
		...mapGetters({
			destination: "getDestination",
			locationId: "getLocationId",
			rootUrl: "getRootUrl",
			userLevel: "getUserLevel",
		}),
	},
	methods: {
		confirmRemoveLink(objectLink) {
			//Send link information up to VueX
			this.$store.commit("updateObjectLink", {
				objectLink,
			});

			//Open the modal
			const modal = new Modal(
				document.getElementById("confirmLinkDeleteModal")
			);
			modal.show();
		},
	}
}
</script>