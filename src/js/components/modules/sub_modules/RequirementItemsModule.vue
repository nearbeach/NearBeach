<template>
    <div>
        <h2><i data-feather="clipboard"></i> Requirement Items</h2>
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
                        <td>Requirement Item</td>
                        <td>Status</td>
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
                                <p class="requirement-item-type">
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
                <a href="javascript:void(0)"
                   class="btn btn-primary save-changes"
                >Create new Requirement Item</a>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');

    export default {
        name: "RequirementItemsModule",
        props: [],
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
            updateItemResults: function() {
                axios.get(
                        'data/items/',
                    ).then((response) => {
                        //Clear the current list
                        this.itemResults = [];

                        //Loop through the results, and push each rows into the array
                        response['data'].forEach((row) => {
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

                        console.log("STATUS: ",response)

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