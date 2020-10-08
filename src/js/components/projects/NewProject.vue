<template>
    <div class="card">
        <div class="card-body">
            <h1>New Project</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        To create a new project, fill out the form and submit at the bottom of the page.
                    </p>
                </div>

                <!-- PROJECT FORM -->
                <div class="col-md-8" style="min-height: 610px;">
                    <!-- PROJECT NAME -->
                    <div class="form-group">
                        <label>Project Name
<!--                            <span class="error" v-if="!$v.projectNameModel.required && $v.projectNameModel.$dirty"-->
<!--                            > Please suppy a title.</span>-->
                        </label>
                        <input type="text"
                               v-model="projectNameModel"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- PROJECT DESCRIPTION -->
                    <label>Project Description:
<!--                        <span class="error" v-if="!$v.documentDescriptionModel.required && $v.documentDescriptionModel.$dirty"> Please supply a scope.</span>-->
<!--                        <span class="error" v-if="!$v.documentDescriptionModel.maxLength"> Sorry - too many characters.</span>-->
                    </label><br>
                    <img src="/static/NearBeach/images/placeholder/body_text.svg"
                         class="loader-image"
                         alt="loading image for Tinymce"
                    />
                    <editor
                       :init="{
                         height: 500,
                         menubar: false,
                         toolbar: 'undo redo | formatselect | ' +
                          'bold italic backcolor | alignleft aligncenter ' +
                          'alignright alignjustify | bullist numlist outdent indent | ',
                       }"
                       v-model="projectDescriptionModel"
                    />
                </div>


            </div>

            <!-- STAKEHOLDER ORGANISATION -->
            <hr>
            <get-stakeholders v-on:update_stakeholder_model="updateStakeholderModel($event)"
            ></get-stakeholders>

            <!-- START DATE & END DATE -->
            <hr>
            <between-dates destination="project"
                           v-on:update_dates="updateDates($event)"
            ></between-dates>

            <!-- Group Permissions -->
            <hr>
            <group-permissions v-bind:group-results="groupResults"
                               v-bind:destination="'project'"
                               v-on:update_group_model="updateGroupModel($event)"
            ></group-permissions>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="submitNewProject"
                    >Create new Project</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import { DateTime } from "luxon";
    import { Modal } from 'bootstrap';

    export default {
        name: "NewProject",
        props: {
            groupResults: Array,
        },
        data() {
            return {
                groupModel: {},
                projectDescriptionModel: '',
                projectEndDateModel: '',
                projectNameModel: '',
                projectStartDateModel: '',
                stakeholderModel: {},
            }
        },
        methods: {
            submitNewProject: function() {
                //Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('project_name',this.projectNameModel);
                data_to_send.set('project_description',this.projectDescriptionModel);
                data_to_send.set('organisation',this.stakeholderModel['value']);
                // data_to_send.set('project_start_date',this.projectStartDateModel);
                // data_to_send.set('project_end_date',this.projectEndDateModel);

                //Get the datetime from start and end date and send as an int of seconds
                var end_date = new Date(this.projectEndDateModel),
                    start_date = new Date(this.projectStartDateModel);

                data_to_send.set('project_start_date', start_date.getTime());
                data_to_send.set('project_end_date',end_date.getTime());

                // Insert a new row for each group list item
                this.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row['value']);
                });

                //Send data to backend
                axios.post(
                    '/new_project/save/',
                    data_to_send
                ).then(response => {
                    //Go to the new project
                    window.location.href = response['data'];
                }).catch(error => {
                    console.log("Error: ",error);
                });
            },
            updateDates: function(data) {
                console.log("DATA: ",data);
                //Update both the start and end dates
                this.projectStartDateModel = data['start_date'];
                this.projectEndDateModel = data['end_date'];
            },
            updateGroupModel: function(data) {
                this.groupModel = data;
            },
            updateStakeholderModel: function(data) {
                this.stakeholderModel = data;
            }
        },
    }
</script>

<style scoped>

</style>