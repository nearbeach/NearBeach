<script setup lang="ts">
import {useI18n} from "petite-vue-i18n";
import {watch, onMounted, ref} from "vue";
import type {ObjectLinkInterface} from "@/utils/interfaces/ObjectLinkInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";
import SmallLoadingSkeleton from "@/components/object_components/skeletons/SmallLoadingSkeleton.vue";
import AddRelationship from "@/components/object_components/link_objects/add_relationship/AddRelationship.vue";
import LinkObjectsTable from "@/components/object_components/link_objects/link_objects_table/LinkObjectsTable.vue";

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
const errorText = ref<string>("");
const isLoaded = ref<boolean>(false);
const objectLinkList = ref<ObjectLinkInterface[]>([]);
const showCreate = ref<boolean>(false);

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
	// Only load data if the object has loaded in
	if (objectStore.is_loaded) {
		await loadData();
	}
});

// Define functions
async function createObjectLink(event: {relationshipModel: string, objectSelectorModel: string}) {
	// Show create
	showCreate.value = true;
	errorText.value = "";

	// Split object selector to get the type and id
	const object_barcode = event.objectSelectorModel.split("-");
	const body = {
		object_type: object_barcode[0],
		object_id: object_barcode[1],
		object_relation: event.relationshipModel,
	};

	await fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/link_list/`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
			body: JSON.stringify(body),
		}
	).then(async (response) => {
		// Notify the user of the change
		showCreate.value = false;

		// Append the value
		const data = await response.json();
		objectLinkList.value.push(data)
	}).catch((error) => {
		errorText.value = error;
	});
}

async function deleteObjectLink(event: {object_assignment_id: number, index: number}) {
	// Remove the link object from the objectLinkList
	objectLinkList.value = objectLinkList.value.filter((_, i: number) => {
		return i !== event.index;
	});

	// Update backend
	await fetch(
		`/api/v1/${objectStore.destination}/${objectStore.id}/link_list/${event.object_assignment_id}/`,
		{
			method: "DELETE",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFTOKEN": getCsrfToken(),
			},
		},
	).catch((error) => {
		errorText.value = error;
	});
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
		errorText.value = error;
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
		<LinkObjectsTable
			v-if="isLoaded"
			ref="link-objects-table"
			:objectLinkList="objectLinkList"
			v-on:delete-object-link="deleteObjectLink"
			v-on:update-relationship="updateRelationship"
		/>
		<SmallLoadingSkeleton v-else>
			{{ t("loading") }}
		</SmallLoadingSkeleton>
		<AddRelationship
			v-if="isLoaded"
			v-on:create-object-link="createObjectLink"
		/>
	</div>
</template>

<style scoped>
.link-objects {
	display: flex;
	flex-direction: column;
}
</style>