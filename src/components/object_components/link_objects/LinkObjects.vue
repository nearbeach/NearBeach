<script setup lang="ts">
import {Plus} from "lucide-vue-next";
import {TrashIcon} from "lucide-vue-next";
import {WlkSelect, WlkButton, required} from "whelk-ui";
import {useI18n} from "petite-vue-i18n";
import {watch, nextTick, onMounted, ref} from "vue";
import RelationshipLink from "@/components/object_components/link_objects/relationship_link/RelationshipLink.vue";
import type {ObjectLinkInterface} from "@/utils/interfaces/ObjectLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import SmallLoadingSkeleton from "@/components/object_components/skeletons/SmallLoadingSkeleton.vue";
import AddRelationship from "@/components/object_components/link_objects/add_relationship/AddRelationship.vue";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			loading: "Loading Object Links",
			select_object: "Select object",
			text: "Connect current object to other objects within NearBeach.",
		},
		ja: {
			loading: "オブジェクトリンク",
			select_object: "オブジェクトを選択",
			text: "ニアビーチ内の現在のオブジェクトを他のオブジェクトに接続する.",
		},
	},
});

// Define stores
const objectStore = useObjectStore();

// Define ref
const addObjectLinkModel = ref<string>("");
const objectLinkList = ref<ObjectLinkInterface[]>([]);
const isLoaded = ref<boolean>(false);

// Watch a specific state property
watch(
	() => objectStore.is_loaded,
	async (new_value) => {
		// If object data is now loaded - fetch data
		if (new_value) {
			await loadData();
		}
	}
)

// Define onMount
onMounted(async () => {
	// Only load data if object has loaded in
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define functions
async function addObjectLink() {
	// ADD CODE
}

async function loadData() {
	// State we are loading
	isLoaded.value = false;

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

async function deleteObjectLink(object_assignment_id: number, index: number) {
	// Remove the link object from the objectLinkList
	objectLinkList.value = objectLinkList.value.filter((_, i: number) => {
		return i !== index;
	});

	// Update backend
	await fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/link_list/${object_assignment_id}/`,
		{
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	).catch((error) => {
		// TODO - handle error's correctly
		console.error(error);
	});
}

function updateRelationship(data: { index: number, link_relationship: string }) {
	let mutated_row = objectLinkList.value[data.index];

	// Check mutated_row exists
	if (mutated_row === undefined) {
		return;
	}

	// Mutate the row
	mutated_row.link_relationship = data.link_relationship;

	// Put the row back in
	objectLinkList.value[data.index] = mutated_row;
}
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
					<p>{{ relationship.object_status }}</p>
					<h4>{{ relationship.object_title }}</h4>
				</div>
				<div class="link-object-status">
					<RelationshipLink
						:index="index"
						:object-assignment-id="relationship.object_assignment_id"
						:object-id="relationship.object_id"
						:object-type="relationship.object_type"
						:relationship="relationship.link_relationship"
						:reverse-relationship="relationship.reverse_relation"
						v-on:update-relationship="updateRelationship"
					/>
				</div>
				<div class="link-object-delete">
					<TrashIcon
						width="20"
						height="20"
						v-on:click="deleteObjectLink(relationship.object_assignment_id, index)"
					/>
				</div>
			</div>
		</div>
		<SmallLoadingSkeleton v-else>
			{{ t("loading") }}
		</SmallLoadingSkeleton>
		<AddRelationship v-if="isLoaded" />
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