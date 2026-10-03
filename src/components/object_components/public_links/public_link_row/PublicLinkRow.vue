<script setup lang="ts">
import {TrashIcon, Check, X} from "@lucide/vue";
import {useI18n} from "petite-vue-i18n";
import {ref} from "vue";

// Define i18n
const {t} = useI18n({
    messages: {
        en: {
            copied_status: "Copied Public Link",
        },
        ja: {
            copied_status: "公開リンクをコピーしました",
        },
    }
})

// Define emits
const emits = defineEmits(['deleteLink', 'updateActive']);

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
const showStatus = ref<boolean>(false);

// Define functions
async function copyLink() {
    // Create the url
    const url = `${window.location.origin}/public_link/${props.id}/`

    // Copy the url to the clipboard
    await navigator.clipboard.writeText(url)
        .then(() => {
            showStatus.value = true;

            setTimeout(() => {
                showStatus.value = false;
            }, 2000);
        })
        .catch((error) => {
            // TODO - handle errors
            console.error("Error copying text: ", error);
        });
}
</script>

<template>
    <td v-on:click="copyLink">
        <span v-if="showStatus"
              class="copied-status"
        >
            {{t("copied_status")}}
        </span>
        <span v-else class="link">{{ id }}</span>
    </td>
    <td v-on:click="emits('updateActive', {id: id, index: index})" >
        <Check v-if="isActive" />
        <X v-else />
    </td>
    <td v-on:click="emits('deleteLink', {id: id})">
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

}
</style>