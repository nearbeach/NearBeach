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
const copyStatusClass = computed(() => {
	return statusError.value ? "copied-status error" : "copied-status";
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
			statusMessage.value = t("public_link_row.copy_error") + " || " + error.message;
			statusError.value = true;
        });
}
</script>

<template>
    <td v-on:click="copyLink">
        <span v-if="statusMessage.length > 0"
              :class="copyStatusClass"
        >
            {{statusMessage}}
        </span>
        <span v-else class="link">{{ id }}</span>
    </td>
    <td v-on:click="emits('updateActive', {id: id, index: index})" >
        <Check v-if="isActive" />
        <X v-else />
    </td>
    <td v-on:click="emits('deleteLink', {id: id})"
		v-if="permissionStore.currentObjectPermissions.currentObject > 1"
	>
        <TrashIcon />
    </td>
</template>

<style scoped>
tr {
    td {
        padding: 0.5rem 0.25rem;
    }

    td > svg {
        width: 15px;
        height: 15px;
    }

	td > .copied-status {
		color: var(--success);

		&.error {
			color: var(--text-red);
		}
	}

}
</style>