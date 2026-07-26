<script setup lang="ts">
import type {PropType} from "vue";
import type {NoteItemInterface} from "@/utils/interfaces/NoteItemInterface.ts";

const props = defineProps({
    noteList: {
        required: true,
        type: Array as PropType<NoteItemInterface[]>
    },
})

</script>

<template>
    <div class="note-list"
        v-if="props.noteList.length > 0"
    >
        <div class="note-item"
             v-for="note in props.noteList"
             :key="note.id"
        >
            {{ note.note }}
        </div>
    </div>
</template>

<style scoped>
.note-list {
    display: flex;
    flex-direction: column;
    border-top: 1px dashed;

    .note-list {

    }
}
</style>