<template>
	<div>
		<div class="row">
			<div class="col-md-4">
				<strong>Card Description</strong>
				<p class="text-instructions">
					Fill out a detailed description for the card, then click on
					the "Update Card" button to update the card.
				</p>
			</div>
			<div class="col-md-8">
				<editor
					license-key="gpl"
					:init="{
						license_key: 'gpl',
						file_picker_types: 'image',
						height: 300,
						images_upload_handler: useUploadImage,
						menubar: false,
						paste_data_images: true,
						plugins: ['lists', 'image', 'codesample', 'table'],
            			toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
					 			'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
            			skin: `${this.skin}`,
			            content_css: `${this.contentCss}`,
						relative_urls: false,
					}"
					v-model="cardDescription"
					v-bind:disabled="editorIsDisabled"
				/>
			</div>
		</div>
		<hr/>

		<div
			class="row"
			v-if="userLevel > 1"
		>
			<div class="col-md-12">
				<button
					class="btn btn-warning"
					v-on:click="closeModal"
				>
					Close & Discard Changes
				</button>
				<button
					class="btn btn-primary save-changes"
					v-on:click="updateCard(true)"
					v-if="kanbanStatus !== 'Closed'"
				>
					Save & Close
				</button>
				<button
					class="btn btn-success save-changes"
					v-on:click="updateCard(false)"
					v-if="kanbanStatus !== 'Closed'"
				>
					Save & Continue
				</button>
			</div>
		</div>
	</div>
</template>

<script>
//TinyMce
import Editor from "@tinymce/tinymce-vue";

//VueX
import {mapGetters} from "vuex";

import {useUploadImage} from "../../composables/uploads/useUploadImage";

export default {
	name: "CardDescription",
	components: {
		editor: Editor,
	},
	emits: [
		"update_card",
	],
	props: {},
	data() {
		return {
			editorIsDisabled: false,
		};
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			kanbanStatus: "getKanbanStatus",
			skin: "getSkin",
			userLevel: "getUserLevel",
		}),
		cardDescription: {
			get() {
				return this.$store.state.card.cardDescription;
			},
			set(value) {
				this.$store.commit("updateValue", {
					field: "cardDescription",
					value,
				});
			},
		},
	},
	methods: {
		useUploadImage,
		closeModal() {
			document
				.getElementById("cardInformationModalCloseButton")
				.click();
		},
		updateCard(close_modal) {
			this.$emit("update_card", {
				close_modal,
			});
		},
	},
	mounted() {
		//BUG - if we use the following condition it won't work. We need to wait at least 500ms before apply it.
		//I hate this :'(
		setTimeout(() => {
			this.editorIsDisabled = this.kanbanStatus === "Closed" || this.userLevel <= 1;
		}, 500);
	}
};
</script>
