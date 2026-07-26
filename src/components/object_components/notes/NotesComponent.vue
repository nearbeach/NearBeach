<script setup lang="ts">
import { WlkButton, WlkTextArea } from "whelk-ui";
import {onMounted, ref, watch} from "vue";
import {useI18n} from "petite-vue-i18n";
import NoteList from "@/components/object_components/notes/note_list/NoteList.vue";
import type {NoteItemInterface} from "@/utils/interfaces/NoteItemInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";

// Define i18n
const {t} = useI18n({
    messages: {
        en: {
            "create": "Submit note",
            "label": "Write a note",
        },
        jp: {
            "create": "メモを作成する",
            "label": "メモを書く",
        },
    }
});

// Define stores
const objectStore = useObjectStore();

// Define ref
const model = ref("");
const noteList = ref<NoteItemInterface[]>([]);

// Define on mounted
onMounted(() => {
   if (objectStore.is_loaded) {
       loadData();
   }
});

// Define watch
watch(
    () => objectStore.is_loaded,
    async (new_value) => {
        // If object data is now loaded - fetch data
        if (new_value) {
            await loadData();
        }
    }
)

// Define functions
async function createNote(): Promise<void> {
    try {
        const body = {
            "note": model.value,
        };

        const response = await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/notes/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body),
            }
        )

        // Get the data
        const data = await response.json();

        // Append to start of the list
        noteList.value.unshift(data);
    } catch (error) {
        // TODO - handle errors properly
        console.error(error);
    }
}

async function loadData(): Promise<void> {
    try {
        const response = await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/notes/`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            }
        );

        // Get the data
        noteList.value = await response.json();
    } catch (error) {
        // TODO - handle errors properly
        console.error(error);
    }
}
</script>

<template>
	<div class="notes">
        <WlkTextArea
            :label="t('label')"
            v-model="model"
        />
        <WlkButton
            class="compact primary"
            @click="createNote"
        >{{t("create")}}</WlkButton>

        <NoteList :note-list="noteList" />
	</div>
</template>

<style scoped>
.notes {

}
</style>