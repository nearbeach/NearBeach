<template>
    <div>
        <strong>{{propertyName}}</strong>
        <span class="error" v-if="!$v.localPropertyList.required && isDirty"> Please create at least one {{propertyName}}.</span>
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
                    <span v-on:click="removeItem(item['id'])">
                        <IconifyIcon v-bind:icon="icons.xCircle"></IconifyIcon>
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


    </div>
</template>

<script>
    import { Modal } from "bootstrap";

    //axios
    const axios = require('axios');

    //Validation
    import { required } from 'vuelidate/lib/validators'

    //Mixins
    import iconMixin from "../../mixins/iconMixin";
import errorModalMixin from '../../mixins/errorModalMixin';

    export default {
        name: "KanbanPropertyOrder",
        props: {
            isDirty: Boolean, //Passes the value from the template above where the checking is done
            isNewMode: {
                type: Boolean,
                default: true,
            },
            kanbanBoardId: {
                type: Number,
                default: 0,
            },
            propertyList: Array,
            propertyName: String,
            source: String,
        },
        data() {
            return {
                localPropertyList: this.propertyList,
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
                this.singleItemId = '';
                this.newPropertyItem = '';

                //Push changes upstream
                this.sendPropertyListUp();

                //Close the modal
                document.getElementById(`addItemClose${this.propertyName}`).click();
            },
            editItem: function(event) {
                //Get the id and title from the item
                this.newPropertyItem = event['target']['dataset']['title'];
                this.singleItemId = event['target']['dataset']['id'];

                //Open up the modal
                this.openModal();
            },
            editModeAddItem: async function(/*var*/) {
                // Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('kanban_column_name', this.newPropertyItem);
                data_to_send.set('kanban_column_sort_number', this.getMaxId() + 1);

                // Send data
                await axios.post(
                    `/kanban_${this.propertyName.toLowerCase()}/${this.kanbanBoardId}/new/`,
                    data_to_send,
                ).then(response => {
                    //Data
                    const data = response['data'][0];
                    const name = `kanban_${this.propertyName.toLowerCase()}_name`;

                    //Add as a new item
                    this.localPropertyList.push({
                        'id': data['pk'],
                        'title': data['name'],
                    });
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
            },
            openModal: function() {
                var newItemModal = new Modal(document.getElementById(`addItem${this.propertyName}`));
                    newItemModal.show();
            },
            removeItem: function(id) {
                //Filter out the id we want to remove
                this.localPropertyList = this.localPropertyList.filter(row => {
                    //Filter out the id we don't want
                    return row['id'] != id;
                });

                //Send the data upstream
                this.sendPropertyListUp();
            },
            sendPropertyListUp: function() {
                this.$emit('update_property_list',{
                    'source': this.source,
                    'data': this.localPropertyList,
                });
            }
        }
    }
</script>

<style scoped>

</style>
