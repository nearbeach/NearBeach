<template>
    <div class="card">
        <h1>New Requirement</h1>
        <hr>
        <div class="grid-x">
            <!-- Description -->
            <div class="small-12 large-4">
                <h3>Description</h3>
                <p>Place a basic helicopter view of the requirement description here. You will be able to break this
                    description down into svaluemaller items using the requirement items below.</p>
            </div>

            <div class="small-12 large-8" style="min-height: 500px;">
                <label>Requirement Title
                    <input id="id_requirement_title"
                           name="requirement_title"
                           type="text"
                           required="true"
                           maxlength="255"
                    />
                </label>
                <img src="static/NearBeach/images/placeholder/body_text.svg"
                     class="loader-image"
                />
                <editor
                   :init="{
                     height: 500,
                     menubar: false,
                     toolbar: 'undo redo | formatselect | ' +
                      'bold italic backcolor | alignleft aligncenter ' +
                      'alignright alignjustify | bullist numlist outdent indent | ',
                   }"
                />
            </div>

            <!-- Stakeholder Organisation -->
            <hr>
            <div class="small-12 large-4">
                <h3>Stakeholder</h3>
                <p>Please search for your stakeholder organisation in the dropdown box. Once found, please select.</p>
            </div>
            <div class="small-12 large-8">
                <label>Stakeholder Organisation
                    <v-select :options="stakeholderFixList"
                              @search="fetchStakeholders"
                              v-model="stakeholderModel"
                              label="stakeholder"
                    />
                </label>
            </div>

            <!-- Status -->
            <hr>
            <div class="small-12 large-4">
                <h3>Status</h3>
                <p>Set the Requirement Status and Type here.</p>
            </div>
            <div class="small-12 large-4">
                <label>Requirement Status
                    <v-select :options="statusFixList"
                              label="status"
                              v-model="statusModel"
                    ></v-select>
                </label>
            </div>
            <div class="small-12 large-4">
                <label>Requirement Type
                    <v-select :options="typeFixList"
                              label="type"
                              v-model="typeModel"
                    ></v-select>
                </label>
            </div>

            <!-- Group Permissions -->
            <hr>
            <group-permissions v-bind:group-results="groupResults"></group-permissions>

            <!-- Submit Button -->
            <hr>
            <div class="cell medium-12 large-12">
                <a href="javascript:void(0)" class="button save-changes">Create new Requirement</a>
            </div>
        </div>
    </div>
</template>

<script>
    //JavaScript components
    import Editor from '@tinymce/tinymce-vue';
    import vSelect from "vue-select";

    const axios = require('axios');

    //Vue components
    import GroupPermissions from '../permissions/GroupPermissions.vue';

    export default {
        name: "NewRequirement",
        components: {
            Editor,
            vSelect,
            GroupPermissions,
        },
        props: [
            'statusList',
            'typeList',
            'groupResults',
        ],
        data() {
            return {
                stakeholderFixList: [],
                stakeholderModel: '',
                statusFixList: [],
                statusModel: '',
                typeFixList: [],
                typeModel: '',
            }
        },
        methods: {
            fetchStakeholders: function() {
                //The following function will use AJAX to obtain a list of 10 (or less) organisations that
                //match the search input.
                axios.post('search/organisation/data')
                    .then(response => {
                        console.log("RESPONSE: ",response);
                    });
            }
        },
        mounted() {
            //We need to extract "fields" array from the statusList/typeList json data
            this.statusList.forEach((row) => {
                //Construct the object
                var construction_object = {
                    'value': row['pk'],
                    'status': row['fields']['requirement_status'],
                };

                //Push the object to status fix list
                this.statusFixList.push(construction_object);
            });
            this.typeList.forEach((row) => {
                //Construct the object
                var construction_object = {
                    'value': row['pk'],
                    'type': row['fields']['requirement_type'],
                }

                //Push the object to type fix list
                this.typeFixList.push(construction_object);
            });
        },
    }
</script>

<style scoped>

</style>