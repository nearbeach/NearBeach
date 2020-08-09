<template>
    <div>
        <h2><i data-feather="clipboard"></i> Requirement Items</h2>
        <p class="text-instructions">
            Requirements should be broken down into smaller compoenents called Requirement Items.
        </p>

        <!-- TABLE OF REQUIREMENT ITEMS -->
        <table class="table table-hover table-stripped">
            <thead>
                <tr>
                    <td>Requirement Item</td>
                    <td>Status</td>
                </tr>
            </thead>
            <tbody>
                <tr v-for="item in itemResults">
                    <td>
                        {{item['fields']['requirement_item_title']}}
                        <br/>
                    </td>
                    <td>{{item['fields']['requirement_item_status']}}</td>
                </tr>
            </tbody>
        </table>
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
                    row['pk'] == status_id;
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
                    row['pk'] == type_id;
                });

                //If there are no results, send back "Unknown Type"
                if (filtered_data.length == 0) {
                    return "Unknown Type";
                }

                //Return the first result
                return filtered_data[0]["fields"]["requirement_item_type"];
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
                        'data/type_status/',
                    ).then((response) => {
                        //Clear the current list
                        this.itemStatusList = [];

                        //Loop through the results, and push each rows into the array
                        response['data'].forEach((row) => {
                            this.itemStatusList.push(row);
                        });
                    });
            },
            updateItemResults: function() {
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