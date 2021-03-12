<template>
    <div>
        <h2><IconifyIcon v-bind:icon="icons.clipboardIcon"></IconifyIcon> Requirement Items</h2>
        <p class="text-instructions">
            Requirements should be broken down into smaller compoenents called Requirement Items.
        </p>

        <!-- TABLE OF REQUIREMENT ITEMS -->
        <div v-if="itemResults.length == 0"
             class="requirement-item-spacer"
        >
            <div class="alert alert-dark">Sorry - there are no Items for this requirement.</div>

        </div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <td width="75%">Requirement Item</td>
                        <td width="25%">Status</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in itemResults">
                        <td>
                            <a v-bind:href="`/requirement_item_information/${item['pk']}/`">
                                <p>
                                    {{item['fields']['requirement_item_title']}}
                                </p>
                                <div class="spacer"></div>
                                <p class="small-text">
                                    Item No. {{item['pk']}} - {{getType(item['fields']['requirement_item_type'])}}
                                </p>
                            </a>
                        </td>
                        <td>{{getStatus(item['fields']['requirement_item_status'])}}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Submit Button -->
        <!-- TO DO - limit it to certain users -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <button v-on:click="createNewItem"
                        class="btn btn-primary save-changes"
                >Create new Requirement Item</button>
            </div>
        </div>

        <!-- NEW REQUIREMENT ITEM MODAL -->
        <new-requirement-item-wizard v-bind:item-status-list="itemStatusList"
                                     v-bind:item-type-list="itemTypeList"
                                     v-bind:location-id="locationId"
                                     v-on:new_item_added="new_item_added($event)"
        ></new-requirement-item-wizard>
    </div>
</template>

<script>
    //JavaScript Libraries
    import {Modal} from "bootstrap";
    const axios = require('axios');

    //Mixins
    import iconMixin from "../../../mixins/iconMixin";

    export default {
        name: "RequirementItemsModule",
        props: [
            'locationId',
        ],
        mixins: [
            iconMixin,
        ],
        components: {
            axios,
        },
        data() {
            return {
                itemResults: [],
                itemStatusList: [],
                itemTypeList: [],
            }
        },
        methods: {
            createNewItem: function() {
                var new_item_modal = new Modal(document.getElementById('newItemModal'));
                new_item_modal.show();
            },
            getStatus: function(status_id) {
                //Filter the status status id
                var filtered_data = this.itemStatusList.filter((row) => {
                    return row['pk'] == status_id;
                });

                //If there are no results, send back "Unknown Status"
                if (filtered_data.length == 0) {
                    return "Unknown Status";
                }

                //Return the first result
                return filtered_data[0]["fields"]["requirement_item_status"];
            },
            getType: function(type_id) {
                //Filter the type id
                var filtered_data = this.itemTypeList.filter((row) => {
                    return row['pk'] == type_id;
                });

                //If there are no results, send back "Unknown Type"
                if (filtered_data.length == 0) {
                    return "Unknown Type";
                }

                //Return the first result
                return filtered_data[0]["fields"]["requirement_item_type"];
            },
            new_item_added: function(data) {
                //A new item has been added in the wizard. We use the new data that has passed through to update
                //the item results array.
                this.itemResults = data;
            },
            updateItemResults: function() {
                axios.get(
                        'data/items/',
                    ).then((response) => {
                        //Clear the current list
                        this.itemResults = [];

                        //Loop through the results, and push each rows into the array
                        response['data'].forEach((row) => {
                            //Update the itemResults
                            this.itemResults.push(row);
                        });
                    });
            },
            updateStatusList: function() {
                axios.get(
                        'data/item_status/',
                    ).then((response) => {
                        //Clear the current list
                        this.itemStatusList = [];

                        //Loop through the results, and push each rows into the array
                        response['data'].forEach((row) => {
                            this.itemStatusList.push(row);
                        });
                    });
            },
            updateTypeList: function() {
                axios.get(
                        'data/item_type/',
                    ).then((response) => {
                        //Clear the current list
                        this.itemTypeList = [];

                        //Loop through the results, and push each rows into the array
                        response['data'].forEach((row) => {
                            this.itemTypeList.push(row);
                        });
                    });
            },

        },
        mounted() {
            this.updateStatusList();
            this.updateTypeList();
            this.updateItemResults();
        }
    }
</script>

<style scoped>

</style>