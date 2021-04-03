<template>
    <div class="modal fade" id="addGroupModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><IconifyIcon v-bind:icon="icons.groupPresentation"></IconifyIcon> Add Group Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="addGroupCloseButton"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <div v-if="groupFixList.length > 0"
                         class="row">
                        <div class="col-md-4">
                            <strong>Add Groups</strong>
                            <p class="text-instructions">
                                Use the following multiple select to select which groups you want to add to this
                                {{destination}}.
                            </p>
                            <p class="text-instructions">
                                Please note: A user's group has to be added to the {{destination}} before the user
                                can be added.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <v-select :options="groupFixList"
                                      v-model="groupModel"
                                      multiple
                            ></v-select>
                        </div>
                    </div>
                    <div v-else
                         class="row"
                    >
                        <div class="col-md-6">
                            <strong>Sorry - no results</strong>
                            <p class="text-instructions">
                                This could be because
                                <ul>
                                    <li>There are no more groups left to add</li>
                                </ul>
                            </p>
                        </div>
                        <div class="col-md-6 no-search">
                            <img src="/static/NearBeach/images/placeholder/questions.svg" alt="Sorry - there are no results" />
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                    >Close</button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="groupModel.length==0"
                            v-on:click="addGroup"
                    >Add Group(s)</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //Mixins
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";

    const axios = require('axios');

    export default {
        name: "AddGroupWizard",
        props: [
            'destination',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                groupFixList: [],
                groupModel: [],
            };
        },
        methods: {
            addGroup: function() {
                //Send the database the new groups to add
                //Get the data_to_send ready
                const data_to_send = new FormData();

                //Loop through the model and append the results
                this.groupModel.forEach(row => {
                    data_to_send.append('group_list',row['value']);
                });

                //user axios
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/add_group/`,
                    data_to_send,
                ).then(response => {
                    //Send the data upstream
                    this.$emit('update_group_list',response['data']);

                    //Close this modal
                    document.getElementById("addGroupCloseButton").click();

                    //Get a new group list
                    this.getGroupList();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            getGroupList: function() {
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/group_list_all/`,
                ).then(response => {
                    //Clear the groupFixList
                    this.groupFixList = [];

                    //Loop through the response's data and add the fixed rows to groupFixList
                    response['data'].forEach(row => {
                        //Create object array
                        var construction_object = {
                            'value': row['pk'],
                            'label': row['fields']['group_name'],
                        };

                        //Add construction_object to groupFixList
                        this.groupFixList.push(construction_object);
                    });
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            }
        },
        mounted() {
            this.getGroupList();
        },
    }
</script>

<style scoped>

</style>
