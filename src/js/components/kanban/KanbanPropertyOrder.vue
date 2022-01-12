<template>
    <div>
        <strong>{{propertyName}}</strong>
        <span class="error" v-if="!v$.localPropertyList.required && isDirty"> Please create at least one {{propertyName}}.</span>
        <br/>

        <!-- The column of data where you can sort the properties -->
        <draggable v-model="localPropertyList"
                   ghost-class="ghost"
                   @change="sendPropertyListUp"
        >
            <transition-group type="transition" name="flip-list" >
                <div v-for="item in localPropertyList"
                     class="sortable"
                     v-bind:key="item['id']"
                     v-bind:id="item['id']"
                     v-bind:data-id="item['id']"
                     v-bind:data-title="item['title']"
                     v-on:dblclick="editItem($event)"
                >
                    <strong v-bind:key="item['id']"
                            v-bind:id="item['id']"
                            v-bind:data-id="item['id']"
                            v-bind:data-title="item['title']"
                    >
                        {{item['title']}}
                    </strong>
                    <span v-on:click="removeItem(item['id'])"
                          v-if="localPropertyList.length > 1"
                    >
                        <Icon v-bind:icon="icons.xCircle"></Icon>
                    </span>
                </div>
            </transition-group>
        </draggable>

        <!-- ADD BUTTON -->
        <hr>
        <button class="btn btn-primary"
                v-on:click="openModal">
            Add {{propertyName}} Item
        </button>

        <!-- MODAL FOR ADDING AN EXTRA ROW -->
        <div class="modal fade"
             v-bind:id="`addItem${propertyName}`"
             tabindex="-1"
             aria-labelledby="exampleModalLabel"
             aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add/Edit {{propertyName}}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" v-bind:id="`addItemClose${propertyName}`"></button>
                    </div>
                    <div class="modal-body">
                        <div class="form-group">
                            <label>{{propertyName}} Item Description</label>
                            <input v-model="newPropertyItem"
                                   type="text"
                                   class="form-control">
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button"
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
        <div class="modal fade"
             v-bind:id="`deleteItem${propertyName}`"
             tabindex="-1"
             aria-labelledby="exampleModalLabel"
             aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Delete {{propertyName}}</h5>
                        <button type="button" 
                                class="btn-close" 
                                data-bs-dismiss="modal" 
                                aria-label="Close" 
                                v-bind:id="`deleteItemClose${propertyName}`"
                        ></button>
                    </div>
                    <div class="modal-body">
                        <!-- CARD DESTINATIONS -->
                        <div class="row">
                            <label><strong>Destination for Cards</strong></label> 
                            <v-select label="title"
                                      values="id"
                                      v-bind:options="newCardDestinationList"
                                      v-model="destinationItemId"
                                      style="z-index:9999"
                                      class="new-card-destination"
                            ></v-select>
                        </div>
                        <br/>

                        <!-- WARNING -->
                        <div class="alert alert-warning">
                            <h4>WARNING</h4>
                            <p>This process can not be reversed. Deleting a {propertyName} will remove it.</p>

                            <p>
                                All existing cards will be moved to the stated location you have provided.
                                Any cards that have been archived or deleted, will still be associated with
                                the removed card.
                            </p>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" 
                                class="btn btn-secondary" 
                                data-bs-dismiss="modal"
                        >
                            Close</button>
                        <button type="button"
                                class="btn btn-primary"
                                v-on:click="deleteItem"
                                v-bind:disabled="this.destinationItemId == null"
                        >
                            Delete {{propertyName}}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import { Modal } from "bootstrap";
    import { Icon } from '@iconify/vue';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required } from '@vuelidate/validators'

    //Mixins
    import iconMixin from "../../mixins/iconMixin";
    import errorModalMixin from '../../mixins/errorModalMixin';

    export default {
        name: "KanbanPropertyOrder",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            Icon,
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
                default: '',
            },
            source: {
                type: String,
                default: '',
            },
        },
        data() {
            return {
                deleteItemId: '',
                destinationItemId: '',
                localPropertyList: this.propertyList,
                newCardDestinationList: [],
                newPropertyItem: '',
                singleItemId: '',
            }
        },
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        validations: {
            localPropertyList: {
                required,
            }
        },
        watch: {
            propertyList: function() {
                this.localPropertyList = this.propertyList;
            },
        },
        methods: {
            addItem: function() {
                //Check to make sure it isn't blank
                if (this.newPropertyItem == '') {
                    return;
                }

                //Depending on the mode (New or Edit) - depends which function we are using
                if (this.isNewMode) {
                    this.newModeAddItem(); 
                } else {
                    this.editModeAddItem();
                }

                //Now that the card has been updated - lets flatten the variables
                //this.singleItemId = '';
                //this.newPropertyItem = '';

                //Push changes upstream
                this.sendPropertyListUp();

                //Close the modal
                document.getElementById(`addItemClose${this.propertyName}`).click();
            },
            deleteItem: function() {
                //Construct the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('delete_item_id',this.deleteItemId);
                data_to_send.set('destination_item_id',this.destinationItemId['id']);

                // URL
                const url = `${this.rootUrl}kanban_${this.propertyName.toLowerCase()}/${this.kanbanBoardId}/delete/`

                //Use axios to send data to backend
                axios.post(
                    url,
                    data_to_send,
                ).then(response => {
                    //Filter out the id we want to remove
                    this.localPropertyList = this.localPropertyList.filter(row => {
                        //Filter out the id we don't want
                        return row['id'] != this.deleteItemId;
                    });

                    //Send the data upstream
                    this.$emit('update_property_list',{
                        'source': this.source,
                        'data': this.localPropertyList,
                    });

                    //Close the dialog
                    document.getElementById(`deleteItemClose${this.propertyName}`).click();
                }).catch(error => {
                    this.showErrorModal(error,'kanban item delete',this.kanbanBoardId) 
                })
            },
            editItem: function(event) {
                //Get the id and title from the item
                this.newPropertyItem = event['target']['dataset']['title'];
                this.singleItemId = event['target']['dataset']['id'];

                //Open up the modal
                this.openModal();
            },
            editModeAddItem: async function(/*var*/) {
                // Create variable names
                const name = `kanban_${this.propertyName.toLowerCase()}_name`,
                      sort_number = `kanban_${this.propertyName.toLowerCase()}_sort_number`,
                      single_item_id = this.singleItemId;

                // Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set(name, this.newPropertyItem);
                data_to_send.set(sort_number, this.getMaxId() + 1);
                
                // Check to see if we are editing an existing item, or adding
                if (single_item_id == '') {
                    //Get the url
                    var url = `/kanban_${this.propertyName.toLowerCase()}/${this.kanbanBoardId}/new/`;
                } else {
                    //Get the url
                    var url = `/kanban_${this.propertyName.toLowerCase()}/${this.singleItemId}/edit/`;
                }

                // Send data
                await axios.post(
                    url,
                    data_to_send,
                ).then(response => {
                    //Data
                    const data = response['data'][0];

                    //Add as a new item
                    if (single_item_id == '') {
                        //Add as a new item
                        this.localPropertyList.push({
                            'id': data['pk'],
                            'title': data['fields'][name],
                        });
                    } else {
                        //Item already exists - edit the item.
                        this.localPropertyList.forEach(row => {
                            //If the id is the same - update the values
                            if (row['id'] == this.singleItemId) {
                                row['title'] = this.newPropertyItem;
                            }
                        });
                    }

                    //Reset variables now we are finished
                    this.singleItemId = '';
                    this.newPropertyItem = '';
                }).catch(error => {
                    this.showErrorModal(error,'kanban board',this.kanbanBoardId) 
                })
            },
            getMaxId: function() {
                //Lets use some math trickery
                const ids = this.localPropertyList.map(property => property['id']);

                //Now lets sort from smallest to largest
                const sorted = ids.sort((a, b) => a - b);

                //Return the last array
                return sorted[ids.length - 1];
            },
            newModeAddItem: function(/*var*/) {
                //NEW MODE -> we are creating a NEW kanban board
                //Depending if there is an ID associated with this depends if we are actually adding an extra item or
                //editing an already existing one.
                if (this.singleItemId == '') {
                    //Add as a new item
                    this.localPropertyList.push({
                        'id': this.getMaxId() + 1,
                        'title': this.newPropertyItem,
                    });
                } else {
                    //Item already exists - edit the item.
                    this.localPropertyList.forEach(row => {
                        //If the id is the same - update the values
                        if (row['id'] == this.singleItemId) {
                            row['title'] = this.newPropertyItem;
                        }
                    });
                }

                //Reset variables 
                this.singleItemId = '';
                this.newPropertyItem = '';
            },
            openModal: function() {
                var newItemModal = new Modal(document.getElementById(`addItem${this.propertyName}`));
                    newItemModal.show();
            },
            removeItem: function(id) {
                if (this.isNewMode) {
                    //Filter out the id we want to remove
                    this.localPropertyList = this.localPropertyList.filter(row => {
                        //Filter out the id we don't want
                        return row['id'] != id;
                    });

                    //Send the data upstream
                    this.sendPropertyListUp();
                } else {
                    //Store the id to delete
                    this.deleteItemId = id;

                    //Create an array of potential destinations for the cards
                    this.newCardDestinationList = this.localPropertyList.filter(row => {
                        return row['id'] != this.deleteItemId;
                    });
                    
                    //Pick the first option by default
                    this.destinationItemId = this.newCardDestinationList[0];

                    //Show the delete modal
                    var deleteItemModal = new Modal(
                        document.getElementById(`deleteItem${this.propertyName}`)
                    );
                    deleteItemModal.show();
                }
            },
            sendPropertyListUp: function() {
                this.$emit('update_property_list',{
                    'source': this.source,
                    'data': this.localPropertyList,
                });
                
                if (!this.isNewMode) {
                    //Use is in Edit mode - send the data to the backend
                    // Check to see if we are editing an existing item, or adding
                    const url = `/kanban_${this.propertyName.toLowerCase()}/${this.kanbanBoardId}/resort/`;
                     
                    //Create data_to_send
                    const data_to_send = new FormData();

                    // Insert a new row for each group list item
                    this.localPropertyList.forEach((row,index) => {
                        data_to_send.append(`item`,row['id']);
                    });

                    axios.post(
                        url,
                        data_to_send,
                    ).then(response => {
                        
                    }).catch(error => {
                        
                    })
                }
            }
        }
    }
</script>

<style scoped>
</style>
