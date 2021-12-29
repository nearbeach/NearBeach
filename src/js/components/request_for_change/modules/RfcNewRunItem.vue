<template>
<div class="modal fade" id="newRunItemModal" tabindex="-1" aria-labelledby="newRunItemModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title" id="newRunItemModalLabel">New Change Task</h2>
                <button type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                        id="newRunItemCloseButton"
                >
                    <span aria-hidden="true"></span>
                </button>
            </div>
            <div class="modal-body">
                <!-- CHANGE TASK TITLE -->
                <div class="row">
                    <div class="col-md-4">
                        <strong>Change Task Title</strong>
                        <p class="text-instructions">
                            Please write a short title of the description for this task. i.e Backup of Database
                        </p>
                    </div>
                    <div class="col-md-8">
                        <div class="form-group">
                            <label>Change Title:</label>
                            <input type="text"
                                   class="form-control"
                                   v-model="changeTitleModel"/>
                        </div>
                    </div>
                </div>

                <!-- START DATE & END DATE -->
                <hr>
                <between-dates destination="Change Task"
                               v-on:update_dates="updateDates($event)"
                ></between-dates>

                <!-- DESCRIPTION OPTIONAL -->
                <hr>
                <div class="row">
                    <div class="col-md-4">
                        <strong>Description</strong>
                        <p class="text-instructions">
                            Write a detail description of this particular task.
                        </p>
                    </div>
                    <div class="col-md-8">
                        <label>Change Task Description (Optional):</label>
                        <editor
                           :init="{
                             height: 300,
                             menubar: false,
                             plugins: 'lists',
                            toolbar: [
                               'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                               'bold italic strikethrough underline backcolor | ' +
                               'bullist numlist outdent indent | removeformat'
                            ]}"
                           v-bind:content_css="false"
                           v-bind:skin="false"
                           v-model="changeDescriptionModel"
                        />
                    </div>
                </div>

                <!-- MISC -->
                <hr>
                <div class="row">
                    <div class="col-md-4">
                        <strong>Misc</strong>
                        <p class="text-instructions">
                            Please fill in the stakeholders for this particular change task. Default value will be
                            "Stakeholders".
                        </p>
                        <p class="text-instructions">
                            To state if there is downtime, please click the "No Downtime" to change it's statue.
                        </p>
                    </div>
                    <div class="col-md-8">
                        <div class="form-group">
                            <label>Stakeholders:</label>
                            <input type="text"
                                   class="form-control"
                                   v-model="changeStakeholderModel"
                            />
                        </div>

                        <br/>
                        <div class="btn-group" role="group" aria-label="Basic checkbox toggle button group">
                            <input type="checkbox"
                                   id="isDowntime"
                                   class="btn-check"
                                   autocomplete="off"
                                   v-model="changeIsDowntimeModel"
                            >
                            <label class="btn btn-outline-primary" for="isDowntime">{{isDowntime()}}</label>
                        </div>
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
                        v-on:click="submitChangeTask($event)"
                >
                    Add Change Task
                </button>
            </div>
        </div>
    </div>
</div> 
</template>

<script>
    const axios = require('axios')

    //Import mixins
    import errorModalMixin from "../../../mixins/errorModalMixin";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "RfcNewRunItem",
        props: {
            locationId: Number,
            rootUrl: {
                type: String,
                default: '/',
            }
        },
        mixins: [
            errorModalMixin,
        ],
        data: () => ({
            changeDescriptionModel: '',
            changeEndDateModel: '',
            changeIsDowntimeModel: false,
            changeStakeholderModel: 'Stakeholder(s)',
            changeStartDateModel: '',
            changeTitleModel: '',
        }),
        computed: {
            ...mapGetters({
                rootUrl: 'getRootUrl',
            })
        },
        methods: {
            isDowntime: function() {
                if (this.changeIsDowntimeModel) {
                    return `Downtime Scheduled`;
                }
                return `No Downtime`;
            },
            submitChangeTask: function(event) {
                //Stop the usual stuff
                event.preventDefault();

                var change_task_seconds = parseInt(this.changeEndDateModel) - parseInt(this.changeStartDateModel)

                // Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('request_for_change', this.locationId.toString());
                data_to_send.set('change_task_title', this.changeTitleModel);
                data_to_send.set('change_task_description', this.changeDescriptionModel);
                data_to_send.set('change_task_start_date', this.changeStartDateModel);
                data_to_send.set('change_task_end_date', this.changeEndDateModel);
                data_to_send.set('change_task_seconds', change_task_seconds.toString());
                // data_to_send.set('change_task_assigned_user', );
                // data_to_send.set('change_task_qa_user', );
                data_to_send.set('change_task_required_by', this.changeStakeholderModel);
                data_to_send.set('is_downtime', this.changeIsDowntimeModel);

                axios.post(
                    `${this.rootUrl}rfc_information/${this.locationId}/new_change_task/`,
                    data_to_send,
                ).then(response => {
                    //Update the runsheet variables
                    this.$emit('update_change_task_list',response['data']);

                    //Clear the modal
                    this.changeDescriptionModel = '';
                    //this.changeEndDateModel = '';
                    this.changeIsDowntimeModel = false;
                    this.changeStakeholderModel = 'Stakeholder(s)';
                    //this.changeStartDateModel = '';
                    this.changeTitleModel = '';

                    //Close the modal
                    document.getElementById("newRunItemCloseButton").click();
                }).catch(error => {
                    this.showErrorModal(error, 'Change Task');
                })

            },
            updateDates: function(data) {
                this.changeStartDateModel = data['start_date'];
                this.changeEndDateModel = data['end_date'];
            },

        }
    }
</script>

<style scoped>

</style>
