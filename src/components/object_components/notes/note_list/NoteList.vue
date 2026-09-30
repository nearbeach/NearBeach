<script setup lang="ts">
import type {PropType} from "vue";
import type {NoteItemInterface} from "@/utils/interfaces/NoteItemInterface.ts";
import {useI18n} from "petite-vue-i18n";
import { Pencil, TrashIcon } from "@lucide/vue";

// Define i18n
const {t} = useI18n({
	messages: {
		en: {
			edit_note: "Edit note",
			empty_note_list: "No notes in object",
			last_modified: "Last Modified",
		},
		ja: {
			edit_note: "編集メモ",
			empty_note_list: "オブジェクトにメモはありません",
			last_modified: "最終更新日時",
		}
	}
})

// Define emits
const emit = defineEmits(['deleteNote', 'editNote']);

const props = defineProps({
	noteList: {
		required: true,
		type: Array as PropType<NoteItemInterface[]>
	},
});


</script>

<template>
	<div class="note-list"
	     v-if="props.noteList.length > 0"
	>
		<div class="note-item"
		     v-for="(note, index) in props.noteList"
		     :key="note.id"
		>
			<div class="author">
				<img class="profile-picture"
				     :src="note.profile_picture"
				     :alt="`${note.first_name}'s profile picture`"
				/>
				<div class="details">
					<div class="name">
						{{ note.first_name }} {{ note.last_name }}
					</div>
					<div class="last-modified">
						<strong>{{t("last_modified")}}: </strong>{{note.date_modified}}
					</div>
				</div>
			</div>
			<div class="note-content">
				{{ note.note }}
			</div>
			<div class="edit-controls">
				<Pencil :aria-label="t('edit_note')"
						v-on:click="emit('editNote', index)"
				/>
				<TrashIcon :aria-label="t('delete_note')"
						   v-on:click="emit('deleteNote', note.id)"
				/>
			</div>
		</div>
	</div>
	<div v-else
	     class="empty-note-list"
	>
		{{ t("empty_note_list") }}
	</div>
</template>

<style scoped>
.note-list {
	display: flex;
	flex-direction: column;
	margin-top: 1.5rem;

	> .note-item {
		padding-top: 0.5rem;
		border-bottom: 1px dashed;

		> .author {
			display: flex;
			flex-direction: row;

			> img {
				width: 40px;
				height: 40px;
				margin-right: 0.5rem;
			}

			> div {
				font-size: 0.75rem;
				font-weight: lighter;
				align-content: center;
				flex-direction: column;

				> .name {
					font-weight: bold;
				}

				> .last-modified {
					font-size: 0.5rem;
					font-weight: lighter;

					> strong {
						font-weight: bold;
					}
				}
			}
		}

		> .note-content {
			margin-top: 0.5rem;
			border: 1px solid grey;
			padding: 0.25rem;
			min-height: 100px;
		}

		> .edit-controls {
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			font-size: 0.75rem;
			margin: 0.25rem 0 0.75rem 0;

			> svg {
				width: 15px;
				height: 15px;
			}
		}

	}
}

.empty-note-list {
	margin-top: 2rem;
	height: 7rem;
	display: flex;
	justify-content: center;
	align-items: center;
	font-size: 1.25rem;
	font-weight: 100;
	font-family: "Roboto", sans-serif;
	border: dashed;
	border-radius: var(--border-radius);
	border-width: var(--border-width);
}
</style>