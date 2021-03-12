<template>
    <div class="modal fade"
             id="newLinkModal"
             tabindex="-1"
             aria-labelledby="linkModal"
             aria-hidden="true"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><IconifyIcon v-bind:icon="icons.linkOut"></IconifyIcon> New {{destination}} Link Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="linkCloseButton"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
                <div class="modal-body">
                    <!-- CHOOSING A OBJECT TYPE -->
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Object Selector</strong>
                            <p class="text-instructions">
                                Please select which object you would like to link to this {{destination}}.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <v-select :options="objectSelection"
                                      v-model="objectModel"
                                      class="object-selection"
                                      v-if="!isSearching"
                            ></v-select>
                            <div v-else
                                 class="alert alert-success"
                            >
                                Searching for {{objectModel}}s
                            </div>
                        </div>
                    </div>
                    <hr>

                    <!-- SELECTING WHICH OBJECTS TO LINK TO -->
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Select Links</strong>
                            <p class="text-instructions">
                                Please select which of the objects you want to connect to this {{destination}}.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <!-- LOADING PLACEHOLDER -->
                            <div id="link_wizard_results"
                                 v-if="isSearching || objectModel == null"
                            >
                                <img src="/static/NearBeach/images/placeholder/search.svg" alt="Searching..." />
                            </div>

                            <div v-if="objectResults.length == 0 && objectModel != null"
                                 class="alert alert-warning"
                            >
                                Sorry - there are no results.
                            </div>

                            <!-- TABLE CONTAINING RESULTS -->
                            <table class="table"
                                   v-if="!isSearching && objectResults.length > 0 && objectModel != null"
                            >
                                <thead>
                                    <tr>
                                        <td>{{objectModel}} Description</td>
                                        <td>Status</td>
                                    </tr>
                                </thead>

                                <!-- PROJECTS -->
                                <tbody v-if="objectModel == 'Project'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="checkbox"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`checkbox_project_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`checkbox_project_${result['pk']}`"
                                                >
                                                    {{result['fields']['project_name']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Project {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['project_status']}}</td>
                                    </tr>
                                </tbody>

                                <!-- TASKS -->
                                <tbody v-if="objectModel == 'Task'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="checkbox"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`checkbox_task_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`checkbox_task_${result['pk']}`"
                                                >
                                                    {{result['fields']['task_short_description']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Task {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['task_status']}}</td>
                                    </tr>
                                </tbody>

                                <!-- REQUIREMENTS -->
                                <tbody v-if="objectModel== 'Requirement'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="checkbox"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`checkbox_requirement_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`checkbox_requirement_${result['pk']}`"
                                                >
                                                    {{result['fields']['requirement_title']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Requirement {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['requirement_status']}}</td>
                                    </tr>
                                </tbody>

                                <!-- REQUIREMENT ITEMS -->
                                <tbody v-if="objectModel== 'Requirement_Item'">
                                    <tr v-for="result in objectResults">
                                        <td>
                                            <div class="form-check">
                                                <input class="form-check-input"
                                                       type="checkbox"
                                                       v-bind:value="result['pk']"
                                                       v-bind:id="`checkbox_requirement_item_${result['pk']}`"
                                                       v-model="linkModel"
                                                >
                                                <label class="form-check-label"
                                                       v-bind:for="`checkbox_requirement_item_${result['pk']}`"
                                                >
                                                    {{result['fields']['requirement_item_title']}}
                                                </label>
                                            </div>
                                            <div class="spacer"></div>
                                            <p class="small-text">Requirement Item {{result['pk']}}</p>
                                        </td>
                                        <td>{{result['fields']['requirement_item_status']}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-bs-dismiss="modal"
                    >
                        Close
                    </button>
                    <button type="button"
                            class="btn btn-primary"
                            v-bind:disabled="linkModel.length==0"
                            v-on:click="saveLinks"
                    >Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    import errorModalMixin from "../../../mixins/errorModalMixin";

    const axios = require('axios');

    export default {
        name: "NewLinkWizard",
        props: {
            destination: String,
            locationId: Number,
        },
        mixins: [
            errorModalMixin,
        ],
        data() {
            return {
                isSearching: false,
                objectModel: null,
                objectResults: [],
                objectSelection: [
                    'Project',
                    'Requirement',
                    'Requirement_Item',
                    'Task',
                ],
                linkModel: [],
            }
        },
        methods: {
            saveLinks: function() {
                // Set up the data object to send
                const data_to_send = new FormData();

                // Go through all link models to add to data_to_send
                this.linkModel.forEach((link) => {
                    data_to_send.append(`${this.objectModel.toLowerCase()}`,link);
                });

                // Use axios to send data
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/add_link/`,
                    data_to_send,
                ).then(response => {
                    //Data has been successfully saved. Time to update the requirement links
                    this.$emit('update_link_results',{});

                    //Click on the close button - a hack, but it should close the modal
                    document.getElementById("linkCloseButton").click();
                });
            }
        },
        watch: {
            objectModel: function() {
                //Clear data
                this.linkModel = [];

                //User has chosen an object.
                if (this.objectModel == null) {
                    //Ok - then removed the objects. We don't need to do anything
                    this.isSearching = false;
                    return;
                }

                //Tell the form that we are searching
                this.isSearching = true;

                //Now to use axios to get the data we require
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/${this.objectModel.toLowerCase()}/link_list/`
                ).then(response => {
                    //Load the data into the array
                    this.objectResults = response['data'];

                    //Tell the user we are no longer searching
                    this.isSearching = false;
                }).catch((error) => {
                    this.showErrorModal(error, this.destination);
                });
            },
        }
    }
</script>

<style scoped>

</style>