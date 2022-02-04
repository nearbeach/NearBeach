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
                        <label>
                            Request for Change Type:
                            <span class="error" v-if="!v$.rfcTypeModel.required && v$.rfcTypeModel.$dirty"
                            > Please suppy a title.</span>
                        </label>
                        <n-select v-bind:options="rfcType"
                                  v-bind:disabled="isReadOnly"
                                  v-model:value="rfcTypeModel"
                        ></n-select>
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
                    <!-- Validation row -->
                    <div class="col-md-12">
                        <span class="error" v-if="checkDateValidation"
                            > Please select an appropriate date for ALL fields.</span>
                    </div>

                    <!-- Dates Row -->
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label>Implementation Start: </label>
                            <n-date-picker type="datetime"
                                      v-model:value="new Date(rfcImplementationStartModel)"
                                      input-class="form-control"
                            ></n-date-picker>
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label>Implementation End: </label>
<!--                            <n-date-picker type="datetime"-->
<!--                                      v-model:value="rfcImplementationEndModel"-->
<!--                                      input-class="form-control"-->
<!--                            ></n-date-picker>-->
                        </div>
                    </div>
                    <div class="col-sm-4">
                        <div class="form-group">
                            <label>Release Date: </label>
<!--                            <n-date-picker type="datetime"-->
<!--                                      v-model:value="rfcReleaseModel"-->
<!--                                      input-class="form-control"-->
<!--                            ></n-date-picker>-->
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
                                    <img v-bind:src="`${staticUrl}/NearBeach/images/placeholder/people_tax.svg`"
                                         alt="default profile"
                                         class="default-user-profile"
                                    />
                                </td>
                                <td>
                                    <strong>{{rfcChangeLead[0]['username']}}: </strong>{{rfcChangeLead[0]['first_name']}} {{rfcChangeLead[0]['last_name']}}
                                    <div class="spacer"></div>
                                    <p class="user-card-email">
                                        {{rfcChangeLead[0]['email']}}
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
                       v-if="userLevel > 1"
                    >Submit RFC for Approval</a>

                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="updateRFC"
                       v-if="userLevel > 1"
                    >Update Request for Change</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import RfcDescription from "./tabs/RfcDescription.vue";
    import { NSelect, NDatePicker } from 'naive-ui';
    
    //Import mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import loadingModalMixin from "../../mixins/loadingModalMixin";

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators'

    export default {
        name: "RfcInformation",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            NDatePicker,
            NSelect,
            RfcDescription,
        },
        props: {
            groupLeaderCount: {
                type: Number,
                default: 0,
            },
            isReadOnly: {
                type: Boolean,
                default: false,
            },
            rfcChangeLead: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            rfcResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            rootUrl: {
                type: String,
                default: '/',
            },
            staticUrl: {
                type: String,
                default: '/',
            },
            userLevel: {
                type: Number,
                default: 0,
            },
        },
        computed: {
            checkDateValidation: function() {
                //Check the validation for each date
                const start_date = !this.v$.rfcImplementationStartModel.required && this.v$.rfcImplementationStartModel.$dirty,
                    end_date = !this.v$.rfcImplementationEndModel.required && this.v$.rfcImplementationEndModel.$dirty,
                    release_date = !this.v$.rfcReleaseModel.required && this.v$.rfcReleaseModel.$dirty;

                //If there is ONE invalidation, we send back true => invalid
                return start_date || end_date || release_date;
            }
        },
        mixins: [
            errorModalMixin,
            loadingModalMixin,
        ],
        data() {
            return {
                rfcChangeLeadFixList: [],
                rfcChangeLeadModel: '',
                rfcTitleModel: this.rfcResults[0]['fields']['rfc_title'],
                rfcSummaryModel: this.rfcResults[0]['fields']['rfc_summary'],
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
        validations: {
            rfcTitleModel: {
                required,
            },
            rfcSummaryModel: {
                required,
                maxLength: maxLength(630000),
            },
            rfcImplementationStartModel: {
                required,
            },
            rfcImplementationEndModel: {
                required,
            },
            rfcReleaseModel: {
                required,
            },
            rfcTypeModel: {
                required,
            },
            rfcVersionModel: {
                maxLength: maxLength(25),
            },
        },
        methods: {
            updateRFC: function() {
                //Check form validation
                this.v$.$touch();

                if (this.v$.$invalid) {
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                const data_to_send = new FormData();
                data_to_send.set('rfc_title',this.rfcTitleModel);
                data_to_send.set('rfc_summary', this.rfcSummaryModel);
                data_to_send.set('rfc_type', this.rfcTypeModel);
                data_to_send.set('rfc_version_number', this.rfcVersionModel);
                data_to_send.set('rfc_implementation_start_date', this.rfcImplementationStartModel);
                data_to_send.set('rfc_implementation_end_date', this.rfcImplementationEndModel);
                data_to_send.set('rfc_implementation_release_date', this.rfcReleaseModel); 

                //Open up the loading modal
                this.showLoadingModal('Project');

                //Use Axios to send the data
                axios.post(
                    `${this.rootUrl}rfc_information/${this.rfcResults[0]['pk']}/save/`,
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
                    `${this.rootUrl}rfc_information/${this.rfcResults[0]['pk']}/update_status/`,
                    data_to_send,
                ).then(response => {
                    //Reload the page to get redirected to the correct place
                    window.location.reload(true);
                }).catch(error => {
                    //Show error if there is one
                    this.showErrorModal(error, 'Request for Change', this.rfcResults[0]['pk']);
                })
            },
            updateValues: function(data) {
                //Update the value
                this[data['modelName']] = data['modelValue'];
            },
        },
        mounted() {
            //Set the type model
            this.rfcTypeModel = this.rfcResults[0]['fields']['rfc_type'];

            //Send root and static url to VueX
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
                staticUrl: this.staticUrl,
            });

            //Send user level to VueX
            this.$store.commit({
                type: 'updateUserLevel',
                userLevel: this.userLevel,
            });
        }
    }
</script>

<style scoped>

</style>
