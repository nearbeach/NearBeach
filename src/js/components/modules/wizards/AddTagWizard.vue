<template>
	<div
		class="modal fade"
		id="addTagModal"
		tabindex="-1"
		aria-labelledby="exampleModalLabel"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h2>
						<Icon v-bind:icon="icons.usersIcon"></Icon>
						Add Tags
						Wizard
					</h2>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
						id="addTagsCloseButton"
					>
						<span aria-hidden="true"></span>
					</button>
				</div>
				<div class="modal-body">
					<div class="row">
						<div class="col-md-4">
							<strong>Add Tag</strong>
							<p class="text-instructions">
								Use the dropdown to select one or many lables to
								add to the {{ destination }}.
							</p>
						</div>
						<div class="col-md-8">
							<label>All Tag List</label>
							<n-select
								label="tag"
								multiple
								:options="tagList"
								v-model:value="tagModel"
							></n-select>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button
						type="button"
						class="btn btn-secondary"
						data-bs-dismiss="modal"
					>
						Close
					</button>
					<button
						type="button"
						class="btn btn-primary"
						v-on:click="addTag"
					>
						Add Tag
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
//JavaScript extras
import iconMixin from "../../../mixins/iconMixin";
import {Icon} from "@iconify/vue";
import {NSelect} from "naive-ui";

//VueX
import {mapGetters} from "vuex";

export default {
	name: "AddTagWizard",
	components: {
		Icon,
		NSelect,
	},
	props: {
		assignedTags: {
			type: Array,
			default: () => {
				return [];
			},
		},
		destination: {
			type: String,
			default: "",
		},
		locationId: {
			type: Number,
			default: 0,
		},
	},
	mixins: [iconMixin],
	data() {
		return {
			allTagList: [],
			tagModel: [],
		};
	},
	computed: {
		...mapGetters({
			rootUrl: "getRootUrl",
		}),
		tagList() {
			return this.allTagList.filter((row) => {
				return (
					this.assignedTags.findIndex((tag) => {
						return tag.pk === parseInt(row.value);
					}) < 0
				);
			});
		},
	},
	methods: {
		addTag() {
			//Construct data_to_send
			const data_to_send = new FormData();

			//Loop through all the models results
			this.tagModel.forEach((row) => {
				data_to_send.append("tag_id", row);
			});

			//Use Axios to send data to backend
			this.axios.post(
				`${this.rootUrl}object_data/${this.destination}/${this.locationId}/add_tags/`,
				data_to_send
			).then((response) => {
				//Emit data up
				this.$emit("add_tags", response.data);

				//Close the modal
				document.getElementById("addTagsCloseButton").click();

				//Clear the results
				this.tagModel = [];
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to add tag",
					message: `Sorry, we could not add tag. Errors -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getTagList() {
			this.axios.post(
				`${this.rootUrl}object_data/tag_list_all/`
			).then((response) => {
				//Map data to the preferred data format for vue-select
				this.allTagList = response.data.map((row) => {
					return {
						value: row.pk,
						label: row.fields.tag_name,
					};
				});
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Failed to get tag list",
					message: `Sorry, we could not get the tag list. Errors -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
	},
	mounted() {
		//If the location is inside the array - don't bother getting the data
		const escape_array = ["requirement_item"];
		if (escape_array.indexOf(this.destination) >= 0) return;

		this.$nextTick(() => {
			//Get the tag list
			this.getTagList();
		});
	},
};
</script>

<style scoped></style>
