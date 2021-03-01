<template>
    <div class="modal fade"
             id="newItemModal"
             tabindex="-1"
             aria-labelledby="requirementItemModal"
             aria-hidden="true"
    >
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h2><i data-feather="clipboard"></i> New Requirement Item Wizard</h2>
                    <button type="button"
                            class="btn-close"
                            data-bs-dismiss="modal"
                            aria-label="Close"
                            id="requirementItemCloseButton"
                    >
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="row">
                        <div class="col-md-4">
                            <strong>Description</strong>
                            <p class="text-instructions">
                                Place in a detailed description of this requirement item. This particular item can be
                                then connected to Project or Tasks.
                            </p>
                        </div>
                        <div class="col-md-8">
                            <label for="id_requirement_item_title">Requirement Item Title:
                                <span class="error" v-if="!$v.requirementItemTitleModel.required"> Please suppy a title.</span>
                            </label>
                            <input id="id_requirement_item_title"
                                   class="form-control"
                                   name="requirement_item_title"
                                   type="text"
                                   required="true"
                                   maxlength="255"
                                   v-model="requirementItemTitleModel"
                            />

                            <br/>
                            <label>Requirement Item Scope:
                                <span class="error" v-if="!$v.requirementItemScopeModel.required && $v.requirementItemScopeModel.$dirty"> Please supply a scope.</span>
                                <span class="error" v-if="!$v.requirementItemScopeModel.maxLength"> Sorry - too many characters.</span>
                            </label><br>
                            <editor
                               :init="{
                                 height: 500,
                                 menubar: false,
                                 toolbar: 'undo redo | formatselect | ' +
                                  'bold italic backcolor | alignleft aligncenter ' +
                                  'alignright alignjustify | bullist numlist outdent indent | ',
                               }"
                               v-bind:content_css="false"
                               v-bind:skin="false"
                               v-model="requirementItemScopeModel"
                            />
                        </div>


                    </div>

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
                                    <span class="error" v-if="!$v.statusItemModel.required && $v.statusItemModel.$dirty"> Please select a status.</span>
                                </label>
                                <v-select :options="statusItemFixList"
                                          label="status"
                                          v-model="statusItemModel"
                                ></v-select>
                            </div>

                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <label>Requirement Type
                                    <span class="error" v-if="!$v.typeItemModel.required && $v.typeItemModel.$dirty"> Please select a type.</span>
                                </label>
                                <v-select :options="typeItemFixList"
                                          label="type"
                                          v-model="typeItemModel"
                                ></v-select>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- FOOTERS -->
                <div class="modal-footer">
                    <button type="button"
                            class="btn btn-secondary"
                            data-dismiss="modal"
                    >
                        Close
                    </button>
                    <button type="button"
                            class="btn btn-primary"
                            v-on:click="saveItem"
                    >Save Requirement Item</button>
                </div>
            </div>
        </div>
</div>
</template>

<script>
    //JavaScript Libraries
    import errorModalMixin from "../../../mixins/errorModalMixin";

    const axios = require('axios');

    //Validation
    import { required, maxLength } from 'vuelidate/lib/validators';

    export default {
        name: "NewRequirementItemWizard",
        props: [
            'itemStatusList',
            'itemTypeList',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
        ],
        data() {
            return {
                requirementItemScopeModel: '',
                requirementItemTitleModel: '',
                statusItemFixList: [],
                statusItemModel: '',
                typeItemFixList: [],
                typeItemModel: '',
            }
        },
        validations: {
            requirementItemScopeModel: {
                required,
                maxLength: maxLength(630000),
            },
            requirementItemTitleModel: {
                required
            },
            statusItemModel: {
                required
            },
            typeItemModel: {
                required
            },
        },
        methods: {
            saveItem: function() {
                // Check the validation first
                this.$v.$touch();

                if (this.$v.$invalid) {
                    //Just return - as we do not need to do the rest of this function
                    return;
                }

                const data_to_send = new FormData();
                data_to_send.set('requirement_item_title', this.requirementItemTitleModel);
                data_to_send.set('requirement_item_scope',this.requirementItemScopeModel);
                data_to_send.set('requirement_item_status',this.statusItemModel['value']);
                data_to_send.set('requirement_item_type',this.typeItemModel['value']);

                axios.post(
                    `/new_requirement_item/save/${this.locationId}/`,
                    data_to_send,
                ).then((response) => {
                    //Data saved successfully - clear all models
                    this.requirementItemScopeModel = '';
                    this.requirementItemTitleModel = '';
                    this.statusItemModel = ''
                    this.typeItemModel = ''

                    //EMIT THE NEW DATA UPSTREAM
                    this.$emit('new_item_added',response['data']);

                    //SHOULD CLOSE MODAL HERE!
                    document.getElementById("requirementItemCloseButton").click();
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })

            },
        },
        watch: {
            itemStatusList: function() {
                //We need to transform the data from the JSON array given to one vue-select can read
                this.itemStatusList.forEach((row) => {
                    //Construct the object
                    var construction_object = {
                        'value': row['pk'],
                        'status': row['fields']['requirement_item_status'],
                    };

                    //Push the object to status fix list
                    this.statusItemFixList.push(construction_object);
                });
            },
            itemTypeList: function() {
                this.itemTypeList.forEach((row) => {
                    //Construct the object
                    var construction_object = {
                        'value': row['pk'],
                        'type': row['fields']['requirement_item_type'],
                    }

                    //Push the object to type fix list
                    this.typeItemFixList.push(construction_object);
                });
            },
        },
    }
</script>

<style scoped>

</style>
