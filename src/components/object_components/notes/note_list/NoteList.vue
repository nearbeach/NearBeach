<script setup lang="ts">
import type {PropType} from "vue";
import type {NoteItemInterface} from "@/utils/interfaces/NoteItemInterface.ts";

// Define emits
const emit = defineEmits(['deleteNote']);

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
		     v-for="note in props.noteList"
		     :key="note.id"
		>
			<div class="author">
					<img class="profile-picture"
						 :src="note.profile_picture"
					     :alt="`${note.first_name}'s profile picture`"
					/>
					<div class="name">
						{{note.first_name}} {{note.last_name}}
					</div>
			</div>
			<div class="note-content">
				{{ note.note }}
			</div>
			<div class="edit-controls">
				<div class="link-object-edit">Edit</div>
				<div class="link-object-delete"
				     v-on:click="emit('deleteNote', note.id)"
				>
					Delete
				</div>
			</div>
		</div>
	</div>
</template>

<style scoped>
.note-list {
	display: flex;
	flex-direction: column;
	margin-top: 2rem;

	> .note-item {
		padding-top: 0.5rem;
		border-top: 1px dashed;

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
			}
		}

		> .note-content {
			margin-top: 0.5rem;
		}

		> .edit-controls {
			display: flex;
			flex-direction: row;
			justify-content: space-between;
			font-size: 0.75rem;
			margin: 0.25rem 0 0.75rem 0;
		}

	}
}
</style>