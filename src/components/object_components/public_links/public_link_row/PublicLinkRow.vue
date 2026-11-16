<script setup lang="ts">
import {TrashIcon, Check, X} from "@lucide/vue";
import {useI18n} from "petite-vue-i18n";
import {computed, ref} from "vue";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

// Define i18n
const {t} = useI18n()

// Define emits
const emits = defineEmits(['deleteLink', 'updateActive']);

// Define store
const permissionStore = usePermissionStore();

// Define props
const props = defineProps({
	id: {
		type: String,
		required: true,
	},
	isActive: {
		type: Boolean,
		required: true,
	},
	index: {
		type: Number,
		required: true,
	},
});

// Define refs
// const showStatus = ref<boolean>(false);
const statusError = ref<boolean>(false);
const statusMessage = ref<string>("");

// Define computed
const updateAriaLabel = computed(() => {
	return props.isActive ? t("public_link_row.deactivate_link") : t("public_link_row.activate_link");
});

const rowName = computed(() => {
	return statusMessage.value.length > 0 ? statusMessage.value : props.id;
})

// Define functions
async function copyLink() {
	// Create the url
	const url = `${window.location.origin}/public_link/${props.id}/`

	// Copy the url to the clipboard
	await navigator.clipboard.writeText(url)
		.then(() => {
			statusMessage.value = t("public_link_row.copied_status");

			setTimeout(() => {
				statusMessage.value = "";
			}, 20000);
		})
		.catch((error) => {
			statusMessage.value = `${t("public_link_row.copy_error")} || ${error.message}`;
			statusError.value = true;
		});
}
</script>

<template>
	<td>
		<button v-on:click="copyLink"
		        class="copy-link-button"
		        type="button"
				:aria-label="t('public_link_row.copy_link')"
		>
			{{ rowName }}
		</button>
	</td>
	<td>
		<button v-on:click="emits('updateActive', {id: id, index: index})"
		        class="active-link-button"
		        type="button"
		        :aria-label="updateAriaLabel"
		>
			<Check v-if="isActive"/>
			<X v-else/>
		</button>
	</td>
	<td v-if="permissionStore.currentObjectPermissions.currentObject > 1">
		<button v-on:click="emits('deleteLink', {id: id})"
				:aria-label="t('public_links.delete_public_link')"
		        class="delete-link-button"
		        type="button"
		>
			<TrashIcon/>
		</button>
	</td>
</template>

<style scoped>
tr {
	td {
		padding: 0;
		margin: 0;

		> button {
			width: 100%;
			padding: 0.5rem;
			border: none;
			background: none;

			&:first-child {
				text-align: left;
			}

			> svg {
				width: 15px;
				height: 15px;
			}
		}

	}
}
</style>