<template>
	<div>
		<strong>{{ propertyName }}</strong>
		<span
			class="error"
			v-if="!v$.localPropertyList.required && isDirty"
		>
			Please create at least one {{ propertyName }}.</span
		>
		<br/>

		<!-- The column of data where you can sort the properties -->
		<draggable
			v-model="localPropertyList"
			:disabled="!canDragCards || isReadOnly"
			item-key="pk"
			ghost-class="ghost"
			@change="sendPropertyListUp"
		>
			<template
				#item="{ element }"
				type="transition"
				name="flip-list"
			>
				<div
					class="sortable"
					v-bind:key="element.id"
					v-bind:id="element.id"
					v-bind:data-property="element.property"
					v-bind:data-id="element.id"
					v-bind:data-title="element.title"
					v-on:dblclick="editItem($event)"
				>
					<strong
						v-bind:key="element.id"
						v-bind:id="element.id"
						v-bind:data-id="element.id"
						v-bind:data-property="element.property"
						v-bind:data-title="element.title"
					>
						{{ element.title }}
					</strong>
					<span
						v-on:click="removeItem(element.id)"
						v-if="localPropertyList.length > 1"
					>
						<Icon v-bind:icon="icons.xCircle"></Icon>
					</span>
				</div>
			</template>
		</draggable>

		<!-- ADD BUTTON -->
		<hr/>
		<button
			class="btn btn-primary"
			v-on:click="openModal"
			v-if="isReadOnly===false"
		>
			Add {{ propertyName }} Item
		</button>

		<!-- MODAL FOR ADDING AN EXTRA ROW -->
		<div
			class="modal fade"
			v-bind:id="`addItem${propertyName}`"
			tabindex="-1"
			aria-labelledby="exampleModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5
							class="modal-title"
							id="exampleModalLabel"
						>
							Add/Edit {{ propertyName }}
						</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
							v-bind:id="`addItemClose${propertyName}`"
						></button>
					</div>
					<div class="modal-body">
						<div class="form-group">
							<label>{{ propertyName }} Item Description</label>
							<input
								v-model="newPropertyItem"
								type="text"
								class="form-control"
							/>
						</div>
						<div
							class="form-group"
							v-if="propertyName.toLowerCase() === 'column'"
						>
							<label>{{ propertyName }} Property</label>
							<n-select
								v-model:value="columnPropertyModel"
								:options="columnPropertyOptions"
							/>
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
							v-on:click="addItem"
						>
							Save changes
						</button>
					</div>
				</div>
			</div>
		</div>

		<!-- MODAL FOR DELETING ITEM -->
		<div
			class="modal fade"
			v-bind:id="`deleteItem${propertyName}`"
			tabindex="-1"
			aria-labelledby="exampleModalLabel"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Delete {{ propertyName }}</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
							v-bind:id="`deleteItemClose${propertyName}`"
						></button>
					</div>
					<div class="modal-body">
						<!-- WARNING -->
						<div class="alert alert-warning">
							<h4>WARNING</h4>
							<p>
								This process can not be reversed. Deleting a
								{{ propertyName }} will remove it.
							</p>

							<p>
								All existing cards will be moved to the stated
								location you have provided. Any cards that have
								been archived or deleted, will still be
								associated with the removed card.
							</p>
						</div>

						<!-- ASK USER ABOUT CARDS -->
						<div class="row">
							<p>Would you like to remove the cards within the {{ propertyName }}?</p>
							<n-radio-group v-model:value="removeCardsModel" name="radiogroup">
								<n-space>
									<n-radio v-bind:value="true"
											 v-bind:label="'Yes - please remove cards'"
									/>
									<n-radio v-bind:value="false"
											 v-bind:label="'No - please MOVE cards'"
									/>
								</n-space>
							</n-radio-group>
						</div>

						<!-- CARD DESTINATIONS -->
						<div class="spacer"></div>
						<div v-if="!removeCardsModel"
							 class="row"
						>
							<p>Please select an appropriate destination for the current cards.</p>
							<label
							><strong>Destination for Cards</strong></label
							>
							<n-select
								v-bind:options="newCardDestinationList"
								v-model:value="destinationItemId"
								style="z-index: 9999"
								class="new-card-destination"
							></n-select>
						</div>
						<br/>


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
							v-if="isReadOnly===false"
							v-on:click="deleteItem"
							v-bind:disabled="this.destinationItemId == null"
						>
							Delete {{ propertyName }}
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import {Modal} from "bootstrap";
import {Icon} from "@iconify/vue";
import {NSelect, NRadioGroup, NRadio, NSpace} from "naive-ui";
import draggable from "vuedraggable";
import {mapGetters} from "vuex";

//Validation
import useVuelidate from "@vuelidate/core";
import {required} from "@vuelidate/validators";

//Mixins
import iconMixin from "../../mixins/iconMixin";

export default {
	name: "KanbanPropertyOrder",
	setup() {
		return {v$: useVuelidate()};
	},
	components: {
		draggable,
		Icon,
		NRadio,
		NRadioGroup,
		NSelect,
		NSpace,
	},
	props: {
		isDirty: {
			type: Boolean,
			default: true,
		}, //Passes the value from the template above where the checking is done
		isNewMode: {
			type: Boolean,
			default: true,
		},
		isReadOnly: {
			type: Boolean,
			default: false,
		},
		kanbanBoardId: {
			type: Number,
			default: 0,
		},
		propertyList: {
			type: Array,
			default: () => {
				return [];
			},
		},
		propertyName: {
			type: String,
			default: "",
		},
		source: {
			type: String,
			default: "",
		},
	},
	data() {
		return {
			columnPropertyModel: "Normal",
			columnPropertyOptions: [
				{
					label: "Backlog",
					value: "Backlog",
				},
				{
					label: "Normal",
					value: "Normal",
				},
				{
					label: "Blocked",
					value: "Blocked",
				},
				{
					label: "Closed",
					value: "Closed",
				},
			],
			deleteItemId: "",
			destinationItemId: "",
			localPropertyList: this.propertyList,
			newCardDestinationList: [],
			newPropertyItem: "",
			removeCardsModel: false,
			singleItemId: "",
		};
	},
	mixins: [iconMixin],
	validations: {
		localPropertyList: {
			required,
		},
	},
	watch: {
		propertyList() {
			this.localPropertyList = this.propertyList;
		},
	},
	computed: {
		...mapGetters({
			canDragCards: "getCanDragCards",
			rootUrl: "getRootUrl",
		}),
	},
	methods: {
		addItem() {
			//Check to make sure it isn't blank
			if (this.newPropertyItem === "") {
				return;
			}

			//Depending on the mode (New or Edit) - depends which function we are using
			if (this.isNewMode) {
				this.newModeAddItem();
			} else {
				this.editModeAddItem();
			}

			//Push changes upstream
			this.sendPropertyListUp();

			//Close the modal
			document.getElementById(
				`addItemClose${this.propertyName}`
			).click();
		},
		deleteItem() {
			//Construct the data_to_send
			const data_to_send = new FormData();
			data_to_send.set("delete_item_id", this.deleteItemId);

			//Only have the destination if remove cards model is false
			if (!this.removeCardsModel) {
				data_to_send.set("destination_item_id", this.destinationItemId);
			}

			// URL
			const url = `${this.rootUrl}kanban_${this.propertyName.toLowerCase()}/${this.kanbanBoardId}/delete/`;

			//Use axios to send data to backend
			this.axios.post(
				url,
				data_to_send
			).then((response) => {
				//Filter out the id we want to remove
				this.localPropertyList = this.localPropertyList.filter(
					(row) => {
						//Filter out the id we don't want
						return row.id !== this.deleteItemId;
					}
				);

				//Send the data upstream
				this.$emit("update_property_list", {
					source: this.source,
					data: this.localPropertyList,
				});

				//Close the dialog
				document.getElementById(
					`deleteItemClose${this.propertyName}`
				).click();
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not delete item",
					message: `Sorry, but we are having issues deleting item - Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		editItem(event) {
			//If read only - ignore
			if (this.isReadOnly) return;

			//Get the id and title from the item
			this.newPropertyItem = event.target.dataset.title;
			this.singleItemId = event.target.dataset.id;
			this.columnPropertyModel = event.target.dataset.property;

			//Open up the modal
			this.openModal();
		},
		editModeAddItem: async function (/*var*/) {
			// Create variable names
			const name = `kanban_${this.propertyName.toLowerCase()}_name`,
				sort_number = `kanban_${this.propertyName.toLowerCase()}_sort_number`,
				single_item_id = this.singleItemId;

			// Create the data_to_send
			const data_to_send = new FormData();
			data_to_send.set(name, this.newPropertyItem);
			data_to_send.set(sort_number, this.getMaxId() + 1);

			//If property name is a column, we add in the column properties as data to send
			if (this.propertyName === "Column") {
				data_to_send.set(
					"kanban_column_property",
					this.columnPropertyModel
				);
			}

			// Check to see if we are editing an existing item, or adding
			if (single_item_id === "") {
				//Get the url
				var url = `/kanban_${this.propertyName.toLowerCase()}/${
					this.kanbanBoardId
				}/new/`;
			} else {
				//Get the url
				var url = `/kanban_${this.propertyName.toLowerCase()}/${
					this.singleItemId
				}/edit/`;
			}

			// Send data
			await this.axios.post(
				url,
				data_to_send
			).then((response) => {
				//Data
				const data = response.data[0];

				//Add as a new item
				if (single_item_id === "") {
					//Add as a new item
					this.localPropertyList.push({
						id: data.pk,
						property: data.fields.kanban_column_property,
						title: data.fields[name],
					});
				} else {
					//Item already exists - edit the item.
					this.localPropertyList.forEach((row) => {
						//If the id is the same - update the values
						if (parseInt(row.id) === parseInt(this.singleItemId)) {
							row.title = this.newPropertyItem;
							row.property = this.columnPropertyModel;
						}
					});
				}

				//Reset variables now we are finished
				this.singleItemId = "";
				this.newPropertyItem = "";
			}).catch((error) => {
				this.$store.dispatch("newToast", {
					header: "Can not add/edit",
					message: `Sorry, but we are having issues editing or adding - Error -> ${error}`,
					extra_classes: "bg-danger",
					delay: 0,
				});
			});
		},
		getMaxId() {
			//Lets use some math trickery
			const ids = this.localPropertyList.map(
				(property) => property.id
			);

			//Now lets sort from smallest to largest
			const sorted = ids.sort((a, b) => a - b);

			//Return the last array
			return sorted[ids.length - 1];
		},
		newModeAddItem(/*var*/) {
			//NEW MODE -> we are creating a NEW kanban board
			//Depending if there is an ID associated with this depends if we are actually adding an extra item or
			//editing an already existing one.
			if (this.singleItemId === "") {
				//Add as a new item
				this.localPropertyList.push({
					id: this.getMaxId() + 1,
					property: this.columnPropertyModel,
					title: this.newPropertyItem,
				});
			} else {
				//Item already exists - edit the item.
				this.localPropertyList.forEach((row) => {
					//If the id is the same - update the values
					if (parseInt(row.id) === parseInt(this.singleItemId)) {
						row.title = this.newPropertyItem;
						row.property = this.columnPropertyModel;
					}
				});
			}

			//Reset variables
			this.singleItemId = "";
			this.newPropertyItem = "";
		},
		openModal() {
			const newItemModal = new Modal(
				document.getElementById(`addItem${this.propertyName}`)
			);
			newItemModal.show();
		},
		removeItem(id) {
			if (this.isNewMode) {
				//Filter out the id we want to remove
				this.localPropertyList = this.localPropertyList.filter(
					(row) => {
						//Filter out the id we don't want
						return row.id !== id;
					}
				);

				//Send the data upstream
				this.sendPropertyListUp();
			} else {
				//Store the id to delete
				this.deleteItemId = id;

				//Create an array of potential destinations for the cards
				this.newCardDestinationList = this.localPropertyList
					.filter((row) => {
						return row.id !== this.deleteItemId;
					})
					.map((row) => {
						return {
							value: row.id,
							label: row.title,
						};
					});

				//Pick the first option by default
				this.destinationItemId =
					this.newCardDestinationList[0].value;

				//Show the delete modal
				const deleteItemModal = new Modal(
					document.getElementById(
						`deleteItem${this.propertyName}`
					)
				);
				deleteItemModal.show();
			}
		},
		sendPropertyListUp() {
			this.$emit("update_property_list", {
				source: this.source,
				data: this.localPropertyList,
			});

			if (!this.isNewMode) {
				//Use is in Edit mode - send the data to the backend
				// Check to see if we are editing an existing item, or adding
				const url = `/kanban_${this.propertyName.toLowerCase()}/${
					this.kanbanBoardId
				}/resort/`;

				//Create data_to_send
				const data_to_send = new FormData();

				// Insert a new row for each group list item
				this.localPropertyList.forEach((row, index) => {
					data_to_send.append("item", row.id);
				});

				this.axios.post(
					url,
					data_to_send
				).catch((error) => {
					this.$store.dispatch("newToast", {
						header: "Can not apply resort",
						message: `Sorry, we've had an issue resorting. Please refresh the page. Error -> ${error}`,
						extra_classes: "bg-danger",
						delay: 0,
					});
				});
			}
		},
	},
};
</script>

<style scoped></style>
