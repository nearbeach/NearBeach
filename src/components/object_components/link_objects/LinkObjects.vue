<script setup lang="ts">
import {TrashIcon} from "lucide-vue-next";
import {useI18n} from "petite-vue-i18n";
import {watch, nextTick, onMounted, ref} from "vue";
import RelationshipLink from "@/components/object_components/link_objects/RelationshipLink/RelationshipLink.vue";
import type {ObjectLinkInterface} from "@/utils/interfaces/ObjectLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import SmallLoadingSkeleton from "@/components/object_components/skeletons/SmallLoadingSkeleton.vue";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			loading: "Loading Object Links",
			text: "Connect current object to other objects within NearBeach.",
		},
		ja: {
			loading: "オブジェクトリンク",
			text: "ニアビーチ内の現在のオブジェクトを他のオブジェクトに接続する.",
		},
	},
});

// Define stores
const objectStore = useObjectStore();

// Define ref
const objectLinkList = ref<ObjectLinkInterface[]>([]);
const isLoaded = ref<boolean>(false);

// Watch a specific state property
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If new_value is false - nothing is loaded
		if (!new_value) {
			return;
		}

		// State we are loading
		isLoaded.value = false;

		console.log("LOADING STUFF");

		// Fetch the required data
		await fetch(
			`/api/v1/${objectStore.destination}/${objectStore.id}/link_list/`,
			{
				method: "GET",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
				},
			},
		).then(async (response) => {
			objectLinkList.value = await response.json();
			isLoaded.value = true;
		}).catch((error) => {
			// TODO - handle error's correctly
			console.error(error);
		});
	}
)

</script>

<template>
	<div class="link-objects">
		<p class="sub-text">{{ t('text') }}</p>
		<div v-if="isLoaded"
			class="link-objects-table"
		>
			<div
				v-for="(relationship, index) of objectLinkList"
				class="link-object"
			>
				<div class="link-object-info">
					<p>{{relationship.object_status}}</p>
					<h4>{{relationship.object_title}}</h4>
				</div>
				<div class="link-object-status">
					<RelationshipLink
						:index="index"
						:relationship="relationship.link_relationship"
						:reverse-relationship="relationship.reverse_relation"
					/>
				</div>
				<div class="link-object-delete">
					<TrashIcon width="20" height="20"/>
				</div>
			</div>
		</div>
		<SmallLoadingSkeleton v-else>
			{{t("loading")}}
		</SmallLoadingSkeleton>
	</div>
</template>

<style scoped>
.link-objects {
	display: flex;
	flex-direction: column;

	> .link-objects-table {
		display: flex;
		flex-direction: column;

		> .link-object {
			display: flex;
			flex-direction: column;
			border: 1px black dashed;
			padding: 1rem 0.5rem 0 0.5rem;
			margin-bottom: 2rem;

			@media (--medium-screen) {
				flex-direction: row;
				padding-right: 3rem;
			}

			@media (--large-screen) {
				padding-right: 0.5rem;
				margin-bottom: 0;
				border-top: none;

				&:first-child {
					border: 1px black dashed;
				}

				&:last-child {
					margin-bottom: 2rem;
				}
			}

			> .link-object-info {
				width: 100%;

				h4 {
					font-size: 1.2rem;
					font-weight: bold;
					margin-bottom: 0.5rem;
				}

				> p {
					margin: 0;
					font-size: 0.875rem;
					font-weight: lighter;
				}
			}

			> .link-object-status {
				width: 100%;

				@media (--medium-screen) {
					width: 30%;
					max-width: 12rem;
				}

				> .wlk-select {
					margin-bottom: 0;
				}
			}

			> .link-object-delete {
				position: absolute;
				left: 100%;
				transform: translate(-2.5rem, -0.25rem);

				& :hover {
					background-color: var(--secondary-hover);
				}

				@media (--medium-screen) {
					transform: translate(-3.75rem, -0.25rem);
				}

				@media (--large-screen) {
					position: inherit;
					transform: translate(0.5rem, -1rem);
					padding: 0.5rem;
				}

				> svg {
					width: 18px;
					height: 18px;
				}
			}
		}
	}


}

</style>