<script setup lang="ts">
import { WlkButton, WlkTextArea, WlkModal, WlkModalHeader, WlkModalFooter } from "whelk-ui";
import {computed, onMounted, ref, watch} from "vue";
import {useI18n} from "petite-vue-i18n";
import NoteList from "@/components/object_components/notes/note_list/NoteList.vue";
import type {NoteItemInterface} from "@/utils/interfaces/NoteItemInterface.ts";
import {useObjectStore} from "@/stores/object/object.ts";
import {getCsrfToken} from "@/composables/getCsrfToken.ts";

// Define i18n
const {t} = useI18n({
    messages: {
        en: {
			cancel_note: "Cancel Note",
            create: "Submit note",
			edit: "Edit note",
            label: "Write a note",
        },
        jp: {
			cancel_note: "メモをキャンセル",
            create: "メモを作成する",
			edit: "編集メモ",
            label: "メモを書く",
        },
    }
});

// Define stores
const objectStore = useObjectStore();

// Define ref
const modalClass = ref<string>("");
const modelId = ref<number | null>(null);
const modelIndex = ref<number>(0);
const modelNote = ref("");
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

// Define computed
const newOrEditNotes = computed(() => {
	return modelId.value === null ? t("create") : t("edit");
})

// Define functions
function closeModal() {
	// Clear the model
	modelId.value = null;
	modelNote.value = "";

	// Clear the modal class
	modalClass.value = "";
}

async function createNote(): Promise<void> {
    try {
        const body = {
            "note": modelNote.value,
        };

        const response = await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/notes/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
	                "X-CSRFTOKEN": getCsrfToken(),
                },
                body: JSON.stringify(body),
            }
        )

        // Get the data
        const data = await response.json();

        // Append to start of the list
        noteList.value.unshift(data);

		// Close modal
		closeModal();
    } catch (error) {
        // TODO - handle errors properly
        console.error(error);
    }
}

async function deleteNote(note_id: number) {
	try {
		await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/notes/${note_id}/`,
            {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
					"X-CSRFTOKEN": getCsrfToken(),
                }
            },
		);

		// Remove note
		noteList.value = noteList.value.filter(row => {
			return row.id !== note_id;
		});
	} catch (error) {
		// TODO - handle errors properly
		console.error(error);
	}
}

async function editNote(index: number): Promise<void> {
	// Check to see if the index exists
	if (noteList.value.length < index + 1) {
		return;
	}

	// Local value
	const note = noteList.value[index];
	if (note === undefined || note === null) {
		return;
	}

	// Update models
	modelId.value = note.id;
	modelIndex.value = index;
	modelNote.value = note.note;

	// Show the modal
	modalClass.value = "open";
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

async function openModal() {
	// New note - clear reference to previous notes
	modelId.value = null;
	modelNote.value = "";

	// Open the modal
	modalClass.value = "open";
}

async function submitNote() {
	// If modelId has a value - we are editing the note - otherwise creating the note
	if (modelId.value === null) {
		// Create the note
		await createNote();
		return;
	}

	// We edit the note
	await updateNote();
}

async function updateNote() {
	try {
        const body = {
            "note": modelNote.value,
        };

        const response = await fetch(
            `/api/v1/${objectStore.destination}/${objectStore.id}/notes/${modelId.value}/`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
	                "X-CSRFTOKEN": getCsrfToken(),
                },
                body: JSON.stringify(body),
            }
        )

		// Local mutation
		let note_row = noteList.value[modelIndex.value];
		if (note_row === undefined) {
			// TODO - Apply an error here
			return;
		}

		// Update the note
		note_row.note = modelNote.value;
		noteList.value[modelIndex.value] = note_row;

		// Close modal
		closeModal();
    } catch (error) {
        // TODO - handle errors properly
        console.error(error);
    }
}
</script>

<template>
	<div class="notes">
		<NoteList
			:note-list="noteList"
			v-on:delete-note="deleteNote"
			v-on:edit-note="editNote"
		/>

		<WlkButton class="compact primary create-note"
				   v-on:click="openModal"
		>
			Create Note
		</WlkButton>

		<teleport to="body">
			<WlkModal :class="modalClass">
				<WlkModalHeader>
					<h3>{{newOrEditNotes}}</h3>
				</WlkModalHeader>
				<WlkTextArea label="" v-model="modelNote" />
				<div class="modal-footer-row">
					<WlkButton class="compact danger"
							   v-on:click="closeModal"
					>
						{{t("cancel_note")}}
					</WlkButton>

					<WlkButton class="compact primary"
							   v-on:click="submitNote"
					>
						{{newOrEditNotes}}
					</WlkButton>
				</div>
			</WlkModal>
		</teleport>
	</div>
</template>

<style scoped>
.notes {
	> .create-note {
		margin-top: 0.5rem;
	}
}

.modal-footer-row {
	display: flex;
	flex-direction: row;
	justify-content: space-between;
}
</style>