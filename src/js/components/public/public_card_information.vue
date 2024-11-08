<template>
	<!-- Card Text -->
	<div class="row">
		<div class="col-md-4">
			<strong>Card Title</strong>
			<p class="text-instructions">
				Write an appropriate name for the kanban card. To update
				click on the "Update" button.
			</p>
		</div>
		<div class="col-md-8">
			<label for="cardText">Card Title</label>
			<input
				type="text"
				id="cardText"
				class="form-control"
				v-bind:value="cardText"
				disabled
			/>
		</div>
	</div>

	<hr/>
	<div class="row">
		<div class="col-md-4">
			<strong>Card Priority</strong>
			<p class="text-instructions">
				Define what the priority of the card is.
			</p>
		</div>
		<div class="col-md-4">
			<label for="cardPriority"
			>
				Card Priority
			</label>
			<input type="text"
				   id="cardPriority"
				   class="form-control"
				   v-bind:value="cardPriority"
				   disabled
			>
		</div>
	</div>
	<hr/>

	<!-- CARD LOCATION -->
	<div class="row">
		<div class="col-md-4">
			<strong>Card Location</strong>
			<p class="text-instructions">
				Select the appropriate location for this card.
			</p>
		</div>

		<div class="col-md-8">
			<div class="row">
				<div class="col-md-6 mt-4">
					<label for="cardColumn"
					>
						Card Column
					</label>
					<input type="text"
						   id="cardColumn"
						   class="form-control"
						   v-bind:value="cardColumn"
						   disabled
					>
				</div>

				<div class="col-md-6 mt-4">
					<label for="cardLevel"
					>
						Card Level
					</label>
					<input type="text"
						   id="cardLevel"
						   class="form-control"
						   v-bind:value="cardLevel"
						   disabled
					>
				</div>
			</div>
		</div>
	</div>

	<hr/>
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
					height: 300,
					menubar: false,
					plugins: ['lists', 'image', 'codesample', 'table'],
            		toolbar: 'undo redo | blocks | bold italic strikethrough underline backcolor | alignleft aligncenter ' +
							 'alignright alignjustify | bullist numlist outdent indent | removeformat | table image codesample',
					skin: `${this.skin}`,
					content_css: `${this.contentCss}`,
					relative_urls: false,
				}"
				v-model="localCardDescription"
				v-bind:disabled="true"
			/>
		</div>
	</div>
</template>

<script>
import editor from "@tinymce/tinymce-vue";

//VueX
import { mapGetters } from "vuex";

export default {
	name: "PublicCardInformation",
	components: {editor},
	props: {
		cardColumn: {
			type: String,
			default: "",
		},
		cardDescription: {
			type: String,
			default: "",
		},
		cardLevel: {
			type: String,
			default: "",
		},
		cardPriority: {
			type: String,
			default: "",
		},
		cardText: {
			type: String,
			default: "",
		},
	},
	computed: {
		...mapGetters({
			contentCss: "getContentCss",
			skin: "getSkin",
		})
	},
	data() {
		return {
			localCardDescription: this.cardDescription,
		};
	},
	watch: {
		cardDescription(new_value) {
			this.localCardDescription = new_value;
		},
	},
}
</script>