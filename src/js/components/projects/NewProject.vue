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
                            <span class="error" v-if="!v$.projectNameModel.required && v$.projectNameModel.$dirty"
                            > Please suppy a title.</span>
                        </label>
                        <input type="text"
                               v-model="projectNameModel"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- PROJECT DESCRIPTION -->
                    <label>Project Description:
                        <span class="error" v-if="!v$.projectDescriptionModel.required && v$.projectDescriptionModel.$dirty"> Please supply a description.</span>
                        <span class="error" v-if="!v$.projectDescriptionModel.maxLength"> Sorry - too many characters.</span>
                    </label><br>
                    <img v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
                         class="loader-image"
                         alt="loading image for Tinymce"
                    />
                    <editor
                       :init="{
                         height: 500,
                         menubar: false,
                         plugins: 'lists',
                         toolbar: [
                             'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                             'bold italic strikethrough underline backcolor | ' +
                             'bullist numlist outdent indent | removeformat'
                        ]}"
                       v-bind:content_css="false"
                       v-bind:skin="false"
                       v-model="projectDescriptionModel"
                    />
                </div>


            </div>

            <!-- STAKEHOLDER ORGANISATION -->
            <hr>
            <get-stakeholders v-on:update_stakeholder_model="updateStakeholderModel($event)"
                              v-bind:is-dirty="v$.stakeholderModel.$dirty"
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
                               v-bind:user-group-results="userGroupResults"
                               v-on:update_group_model="updateGroupModel($event)"
                               v-bind:is-dirty="v$.groupModel.$dirty"
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
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators';
    import BetweenDates from "../dates/BetweenDates.vue";
    import StakeholderInformation from "../organisations/StakeholderInformation.vue";
    import Editor from '@tinymce/tinymce-vue';
    import GroupPermissions from "../permissions/GroupPermissions.vue";
    import GetStakeholders from "../organisations/GetStakeholders.vue";

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    export default {
        name: "NewProject",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            BetweenDates,
            'editor': Editor,
            GetStakeholders,
            GroupPermissions,
            StakeholderInformation,
        },
        props: {
            groupResults: Array,
            rootUrl: {
                type: String,
                default: "/",
            },
            staticUrl: {
                type: String,
                default: "/",
            },
            userGroupResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        mixins: [
            errorModalMixin,
        ],
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
        validations: {
            groupModel: {
                required,
            },
            projectDescriptionModel: {
                required,
                maxLength: maxLength(630000),
            },
            projectEndDateModel: {
                required
            },
            projectNameModel: {
                required
            },
            projectStartDateModel: {
                required
            },
            stakeholderModel: {
                required
            },
        },
        methods: {
            submitNewProject: async function() {
                //Check validation
                const isFormCorrect = await this.v$.$validate();

                if (!isFormCorrect && (
                    this.v$.groupModel.$error.length > 0 ||
                    this.v$.stakeholderModel.length > 0 ||
                    this.v$.projectDescriptionModel.length > 0 ||
                    this.v$.projectEndDateModel.length > 0 ||
                    this.v$.projectNameModel.length > 0 ||
                    this.v$.projectStartDateModel.length > 0
                )) {
                    this.showValidationErrorModal();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                //Create data_to_send
                const data_to_send = new FormData();
                data_to_send.set('project_name',this.projectNameModel);
                data_to_send.set('project_description',this.projectDescriptionModel);
                data_to_send.set('organisation',this.stakeholderModel);
                data_to_send.set('project_start_date',this.projectStartDateModel.toISOString());
                data_to_send.set('project_end_date',this.projectEndDateModel.toISOString());

                // Insert a new row for each group list item
                this.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row);
                });

                //Send data to backend
                axios.post(
                    `${this.rootUrl}new_project/save/`,
                    data_to_send
                ).then(response => {
                    //Go to the new project
                    window.location.href = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            },
            updateDates: function(data) {
                //Update both the start and end dates
                this.projectStartDateModel = new Date(data['start_date']);
                this.projectEndDateModel = new Date(data['end_date']);
            },
            updateGroupModel: function(data) {
                this.groupModel = data;
            },
            updateStakeholderModel: function(data) {
                this.stakeholderModel = data;
            }
        },
        mounted() {
            //Map the results from the user_group_results to groupModels
            /*
            setTimeout(() => {
                this.groupModel = this.userGroupResults.map(row => {
                    return {
                        group: row['group__group_name'],
                        value: row['group_id'],
                    }
                });
            },100);
            */

            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
            });
        },
    }
</script>

<style scoped>

</style>
