<template>
    <div class="card">
        <div class="card-body">
            <h1>New Requirement</h1>
            <hr>
            <div class="row">
                <!-- Description -->
                <div class="col-md-4">
                    <h2>Description</h2>
                    <p class="text-instructions">
                        Place a basic bird's eye view of the requirement description here. You will be able to break
                        the requirement down into smaller components called 'Items' on the next page.
                    </p>
                </div>

                <div class="col-md-8" style="min-height: 610px;">
                    <div class="form-group">
                        <label for="id_requirement_title">Requirement Title:
                            <span class="error" v-if="!v$.requirementTitleModel.required && v$.requirementTitleModel.$dirty"> Please suppy a title.</span>
                        </label>
                        <input id="id_requirement_title"
                               class="form-control"
                               name="requirement_title"
                               type="text"
                               required="true"
                               maxlength="255"
                               v-model="requirementTitleModel"
                        />
                    </div>

                    <br/>
                    <label>Requirement Scope:
                        <span class="error" v-if="!v$.requirementScopeModel.required && v$.requirementScopeModel.$dirty"> Please supply a scope.</span>
                        <span class="error" v-if="!v$.requirementScopeModel.maxLength"> Sorry - too many characters.</span>
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
                       v-model="requirementScopeModel"
                    />
                </div>
            </div>

            <!-- Stakeholder Organisation -->
            <hr>
            <get-stakeholders v-on:update_stakeholder_model="updateStakeholderModel($event)"
                              v-bind:is-dirty="v$.stakeholderModel.$dirty"
            ></get-stakeholders>

            <!-- Status -->
            <hr>
            <div class="row">
                <div class="col-md-4">
                    <h2>Status</h2>
                    <p class="text-instructions">Set the Requirement Status and Type here.</p>
                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Requirement Status
                            <span class="error" v-if="!v$.statusModel.required && v$.statusModel.$dirty"> Please select a status.</span>
                        </label>
                        <n-select :options="statusFixList"
                                  label="status"
                                  v-model:value="statusModel"
                        ></n-select>
                    </div>

                </div>
                <div class="col-md-4">
                    <div class="form-group">
                        <label>Requirement Type
                            <span class="error" v-if="!v$.typeModel.required && v$.typeModel.$dirty"> Please select a type.</span>
                        </label>
                        <n-select :options="typeFixList"
                                  label="type"
                                  v-model:value="typeModel"
                        ></n-select>
                    </div>
                </div>
            </div>

            <!-- Group Permissions -->
            <hr>
            <group-permissions v-bind:group-results="groupResults"
                               v-bind:destination="'requirement'"
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
                       v-on:click="submitNewRequirement"
                    >Create new Requirement</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript Libraries
    const axios = require('axios');
    import { Modal } from 'bootstrap';
    import Editor from '@tinymce/tinymce-vue';
    import GetStakeholders from "../organisations/GetStakeholders.vue";
    import GroupPermissions from "../permissions/GroupPermissions.vue";
    import { NSelect } from 'naive-ui';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required, maxLength } from '@vuelidate/validators'

    export default {
        name: "NewRequirement",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            axios,
            'editor': Editor,
            GetStakeholders,
            GroupPermissions,
            NSelect,
        },
        props: {
            groupResults: {
                type: Array,
                return: () => {
                    return [];
                },
            },
            rootUrl: {
                type: String,
                default: '/',
            },
            staticUrl: {
                type: String,
                default: "/",
            },
            statusList: {
                type: Array,
                return: () => {
                    return [];
                },
            },
            typeList: {
                type: Array,
                return: () => {
                    return [];
                },
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
                groupModel: '',
                requirementScopeModel: '',
                requirementTitleModel: '',
                stakeholderModel: '',
                statusFixList: [],
                statusModel: '',
                typeFixList: [],
                typeModel: '',
            }
        },
        validations: {
            groupModel: {
                required,
            },
            requirementScopeModel: {
                required,
                maxLength: maxLength(630000),
            },
            requirementTitleModel: {
                required
            },
            stakeholderModel: {
                required
            },
            statusModel: {
                required
            },
            typeModel: {
                required
            },
        },
        methods: {
            submitNewRequirement: async function() {
                // Check the validation first
                const isFormCorrect = await this.v$.$validate();

                if (!isFormCorrect && (
                    this.v$.groupModel.$error.length > 0 ||
                    this.v$.stakeholderModel.length > 0 ||
                    this.v$.requirementTitleModel.length > 0 ||
                    this.v$.requirementScopeModel.length > 0 ||
                    this.v$.statusModel.length > 0 ||
                    this.v$.typeModel.length > 0
                )) {
                    //Show the error dialog and notify to the user that there were field missing.
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML =
                        `<strong>FORM ISSUE:</strong> Sorry, but can you please fill out the form completely.`;

                    // Show the modal
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();

                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                // Set up the data object to send
                const data_to_send = new FormData();
                data_to_send.set('requirement_title', this.requirementTitleModel);
                data_to_send.set('requirement_scope',this.requirementScopeModel);
                data_to_send.set('organisation',this.stakeholderModel);
                data_to_send.set('requirement_status',this.statusModel);
                data_to_send.set('requirement_type',this.typeModel);

                // Insert a new row for each group list item
                this.groupModel.forEach((row,index) => {
                    data_to_send.append(`group_list`,row);
                });

                // Use Axion to send the data
                axios.post(
                    'save/',
                    data_to_send
                ).then((response) => {
                    // Use the result to go to the url
                    window.location.href = response['data']
                }).catch((error) => {
                    // Get the error modal
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML = `<strong>HTML ISSUE:</strong> We could not save the new requirement<hr>${error}`;

                    // Show the modal
                    //var errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
                    var errorModal = new Modal(document.getElementById('errorModal'));
                    errorModal.show();
                });
            },
            updateGroupModel: function(newGroupModel) {
                //Update the group model
                this.groupModel = newGroupModel;
            },
            updateStakeholderModel: function(newStakeholderModel) {
                this.stakeholderModel = newStakeholderModel;
            }
        },
        mounted() {
            //VueX
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
                staticUrl: this.staticUrl,
            })

            //We need to map "fields" array from the statusList/typeList json data
            this.statusFixList = this.statusList.map((row) => {
                return {
                    value: row['pk'],
                    label: row['fields']['requirement_status'],
                };
            });

            this.typeFixList = this.typeList.map((row) => {
                return {
                    value: row['pk'],
                    label: row['fields']['requirement_type'],
                }
            });
        },
    }
</script>

<style scoped>

</style>
