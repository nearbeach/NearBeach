<template>
    <div class="card">
        <div class="card-body">
            <h1>Request for Change</h1>
            <hr>

            <rfc-description v-bind:rfc-results="rfcResults"
                             v-bind:is-read-only="isReadOnly"
                             v-on:update_values="updateValues($event)"
            ></rfc-description>

            <!-- Request for Change Types and Release Number -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <h2>Type and Version</h2>
                    <p class="text-instructions">
                        Please specify how urgent this RFC's status really is. Optionally you can also specify the version
                        or release number.
                    </p>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Request for Change Type: </label>
                        <v-select v-bind:options="rfcType"
                                  v-bind:disabled="isReadOnly"
                                  v-model="rfcTypeModel"
                        ></v-select>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Version/Release Number</label>
                        <input type="text"
                               maxlength="25"
                               class="form-control"
                               v-model="rfcVersionModel"
                        />
                    </div>
                </div>
            </div>

            <!-- Implementation and Release Dates -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <h2>Important Dates</h2>
                    <p class="text-instructions">
                        Please supply the implementation start and end dates. Please also suply the release date of the
                        change to the general consumer.
                    </p>
                </div>
                <div class="row col-md-8">
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label>Implementation Start: </label>
                            <datetime type="datetime"
                                      v-model="rfcImplementationStartModel"
                                      input-class="form-control"
                                      v-bind:minute-step="5"
                            ></datetime>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label>Implementation End: </label>
                            <datetime type="datetime"
                                      v-model="rfcImplementationEndModel"
                                      input-class="form-control"
                                      v-bind:minute-step="5"
                            ></datetime>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label>Release Date: </label>
                            <datetime type="datetime"
                                      v-model="rfcReleaseModel"
                                      input-class="form-control"
                                      v-bind:minute-step="5"
                            ></datetime>
                        </div>
                    </div>
                </div>
            </div>

            <!-- RFC Change Lead User -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <h2>Change LEAD: </h2>
                    <p class="text-instructions">
                        Please supply the LEAD who will be leading this Request for Change.
                    </p>
                </div>
                <div class="col-md-4">
                    <table class="table user-table-module">
                        <tbody>
                            <tr>
                                <td>
                                    <img src="/static/NearBeach/images/placeholder/people_tax.svg" alt="default profile" class="default-user-profile" />
                                </td>
                                <td>
                                    <strong>{{rfcChangeLead[0]['fields']['username']}}: </strong>{{rfcChangeLead[0]['fields']['first_name']}} {{rfcChangeLead[0]['fields']['last_name']}}
                                    <div class="spacer"></div>
                                    <p class="user-card-email">
                                        {{rfcChangeLead[0]['fields']['email']}}
                                    </p>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Update Button -->
            <hr v-if="!isReadOnly">
            <div class="row submit-row"
                 v-if="!isReadOnly"
            >
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-dark"
                       v-on:click="updateRFCStatus"
                    >Submit RFC for Approval</a>

                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateRFC"
                    >Update Request for Change</a>
                </div>
            </div>

            <!-- Approval Buttons -->
            <!-- Only show this section when;
                - is Read Only
                - RFC Status is waiting for approval
                - User is a group leader (groupLeaderCount > 0)
            -->
            <hr v-if="showApprovalButton">
            <div class="row submit-row"
                 v-if="showApprovalButton"
            >
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary"
                       v-on:click=""
                    >Approve RFC</a>

                    <a href="javascript:void(0)"
                       class="btn btn-danger reject-rfc"
                       v-on:click=""
                    >REJECT RFC</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    
    //Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    export default {
        name: "RfcInformation",
        props: {
            groupLeaderCount: {
                type: Number,
                default: 0,
            },
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            rfcChangeLead: Array,
            rfcResults: Array,
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        data() {
            return {
                rfcChangeLeadFixList: [],
                rfcChangeLeadModel: '',
                rfcData: {
                    'rfcTitleModel': this.rfcResults[0]['fields']['rfc_title'],
                    'rfcSummaryModel': this.rfcResults[0]['fields']['rfc_summary'],
                },
                rfcImplementationStartModel: this.rfcResults[0]['fields']['rfc_implementation_start_date'],
                rfcImplementationEndModel: this.rfcResults[0]['fields']['rfc_implementation_end_date'],
                rfcReleaseModel: this.rfcResults[0]['fields']['rfc_implementation_release_date'],
                rfcStatus: [
                    { label: 'Draft', value: 1 },
                    { label: 'Waiting for approval', value: 2 },
                    { label: 'Approved', value: 3 },
                    { label: 'Started', value: 4 },
                    { label: 'Finished', value: 5 },
                    { label: 'Rejected', value: 6 },
                ],
                rfcType: [
                    { label: 'Emergency', value: 4 },
                    { label: 'High', value: 3 },
                    { label: 'Medium', value: 2 },
                    { label: 'Low', value: 1 },
                ],
                rfcTypeModel: '',
                rfcVersionModel: this.rfcResults[0]['fields']['rfc_version_number'],
            }
        },
        computed: {
            showApprovalButton: function() {
                // Only show this section when;
                // - is Read Only
                // - RFC Status is waiting for approval
                // - User is a group leader (groupLeaderCount > 0)
                return this.isReadOnly && this.rfcResults[0]['fields']['rfc_status'] === 2 && this.groupLeaderCount > 0;
            },
        },
        methods: {
            updateRFC: function() {
                const data_to_send = new FormData();
                data_to_send.set('rfc_title',this.rfcData['rfcTitleModel']); //TODO FIND OUT WHERE THIS VALUE IS!!!
                data_to_send.set('rfc_summary', this.rfcData['rfcSummaryModel']); //TODO FIND OUT WHERE THIS VALUES IS!!!
                data_to_send.set('rfc_type', this.rfcTypeModel['value']);
                data_to_send.set('rfc_version_number', this.rfcVersionModel);
                data_to_send.set('rfc_implementation_start_date', this.rfcImplementationStartModel);
                data_to_send.set('rfc_implementation_end_date', this.rfcImplementationEndModel);
                data_to_send.set('rfc_implementation_release_date', this.rfcReleaseModel); 

                //Open up the loading modal
                this.showLoadingModal('Project');

                //Use Axios to send the data
                axios.post(
                    `/rfc_information/${this.rfcResults[0]['pk']}/save/`,
                    data_to_send,
                ).then(response => {
                    //Notify user of success update
                    this.closeLoadingModal();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            },
            updateRFCStatus: function() {
                const data_to_send = new FormData();
                data_to_send.set('rfc_status','2'); //Value 2: Waiting for Approval

                axios.post(
                    `/rfc_information/${this.rfcResults[0]['pk']}/update_status/`,
                    data_to_send,
                ).then(response => {
                    //Reload the page to get redirected to the correct place
                    window.location.reload(true);
                }).catch(error => {
                    //ADD MIXIN
                })
            },
            updateValues: function(data) {
                //Update the value
                this.rfcData[data['modelName']] = data['modelValue'];
            },
        },
        mounted() {
            //Set the type model
            this.rfcTypeModel = this.rfcType.filter(row => {
                //Filter for just the one value result
                return row['value'] == this.rfcResults[0]['fields']['rfc_type'];
            })[0];
        }
    }
</script>

<style scoped>

</style>
