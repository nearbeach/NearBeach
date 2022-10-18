<template>
    <div class="card">
        <div class="card-body">
            <h1>New Task</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        To create a new task, fill out the form and submit at the bottom of the page.
                    </p>

                    <p class="text-instructions">
                        <strong>Note: </strong>Media files can not be uploaded until AFTER you save.
                        This is a security feature.
                    </p>
                </div>

                <!-- Task FORM -->
                <div class="col-md-8" style="min-height: 610px;">
                    <!-- TASK NAME -->
                    <div class="form-group">
                        <label>Task Short Description:
                            <span class="error"
                                  v-if="!v$.taskShortDescriptionModel.$error.length > 0"
                            > Please supply a title.</span>
                        </label>
                        <input type="text"
                               v-model="taskShortDescriptionModel"
                               class="form-control"
                        >
                    </div>
                    <br/>

                    <!-- TASK DESCRIPTION -->
                    <label>Task Long Description:
                        <span class="error" v-if="!v$.taskDescriptionModel.$error.length > 0"
                        > Please supply a description.</span>
                    </label><br>
                    <img v-bind:src="`${staticUrl}NearBeach/images/placeholder/body_text.svg`"
                         class="loader-image"
                         alt="loading image for Tinymce"
                    />
                    <editor
                       :init="{
                         height: 500,
                         menubar: false,
                         plugins: ['lists','table'],
                        toolbar: [
                           'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                           'bold italic strikethrough underline backcolor | table | ' +
                           'bullist numlist outdent indent | removeformat'
                        ]}"
                       v-bind:content_css="false"
                       v-bind:skin="false"
                       v-model="taskDescriptionModel"
                    />
                </div>


            </div>

            <!-- STAKEHOLDER ORGANISATION -->
            <hr>
            <get-stakeholders v-on:update_stakeholder_model="updateStakeholderModel($event)"
                              v-bind:is-dirty="v$.stakeholderModel.$error.length > 0"
            ></get-stakeholders>

            <!-- START DATE & END DATE -->
            <hr>
            <between-dates destination="task"
                           v-on:update_dates="updateDates($event)"
            ></between-dates>

            <!-- Group Permissions -->
            <hr>
            <group-permissions v-bind:group-results="groupResults"
                               v-bind:destination="'task'"
                               v-bind:user-group-results="userGroupResults"
                               v-on:update_group_model="updateGroupModel($event)"
                               v-bind:is-dirty="v$.groupModel.$error.length > 0"
            ></group-permissions>

            <!-- Submit Button -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <a href="javascript:void(0)"
                       class="btn btn-primary save-changes"
                       v-on:click="submitNewTask"
                    >Create new Task</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators'
    import Editor from '@tinymce/tinymce-vue'
    import BetweenDates from "../dates/BetweenDates.vue";
    import GroupPermissions from "../permissions/GroupPermissions.vue";
    import GetStakeholders from "../organisations/GetStakeholders.vue";

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    export default {
        name: "NewTask",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            BetweenDates,
            GetStakeholders,
            GroupPermissions,
            'editor': Editor,
        },
        props: {
            groupResults: {
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
            userGroupResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        data() {
            return {
                groupModel: {},
                stakeholderModel: '',
                taskDescriptionModel: '',
                taskEndDateModel: '',
                taskShortDescriptionModel: '',
                taskStartDateModel: '',
            }
        },
        mixins: [
            errorModalMixin,
        ],
        validations: {
            groupModel: {
                required,
            },
            stakeholderModel: {
                required,
            },
            taskDescriptionModel: {
                required,
                maxLength: maxLength(630000),
            },
            taskEndDateModel: {
                required,
            },
            taskShortDescriptionModel: {
                required,
            },
            taskStartDateModel: {
                required,
            },
        },
        methods: {
            submitNewTask: async function() {
                //Check validation
                const isFormCorrect = await this.v$.$validate();

                //If the form is not validated
                if (!isFormCorrect && (
                    this.v$.groupModel.$error.length > 0 ||
                    this.v$.stakeholderModel.length > 0 ||
                    this.v$.taskDescriptionModel.length > 0 ||
                    this.v$.taskEndDateModel.length > 0 ||
                    this.v$.taskShortDescriptionModel.length > 0 ||
                    this.v$.taskStartDateModel.length > 0
                )) {
                    this.showValidationErrorModal();

                    //User does not need to do anything else
                    return;
                }

                //Create the data_to_send array
                const data_to_send = new FormData();
                data_to_send.set('organisation',this.stakeholderModel);
                data_to_send.set('task_long_description',this.taskDescriptionModel);
                data_to_send.set('task_end_date',this.taskEndDateModel.toISOString());
                data_to_send.set('task_short_description',this.taskShortDescriptionModel);
                data_to_send.set('task_start_date',this.taskStartDateModel.toISOString());

                // Insert a new row for each group list item
                this.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row);
                });

                //Send data to backend
                axios.post(
                    'save/',
                    data_to_send
                ).then(response => {
                    //Go to the new project
                    window.location.href = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                });
            },
            updateDates: function(data) {
                this.taskEndDateModel = new Date(data['end_date']);
                this.taskStartDateModel = new Date(data['start_date']);
            },
            updateGroupModel: function(data) {
                this.groupModel = data;
            },
            updateStakeholderModel: function(data) {
                this.stakeholderModel = data;
            }
        },
        mounted() {
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
                staticUrl: this.staticUrl,
            })
        },
    }
</script>

<style scoped>

</style>
