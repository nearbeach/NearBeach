<template>
    <div>
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
                <div class="form-group">
                    <label>LEAD: </label>
                    <v-select :options="[{label: 'Canada', code: 'ca'}]"
                              v-model="rfcChangeLead"
                    ></v-select> <!-- TO DO FIX THIS -->
                </div>
            </div>
        </div>


        <!-- Group Permissions -->
        <hr>
        <group-permissions v-bind:group-results="groupResults"
                           v-bind:destination="'project'"
                           v-on:update_group_model="updateGroupModel($event)"
        ></group-permissions>
    </div>
</template>

<script>
    export default {
        name: "RfcDetails",
        props: {
            groupResults: Array,
            userResults: Array,
        },
        data() {
            return {
                rfcChangeLead: '',
                rfcImplementationStartModel: '',
                rfcImplementationEndModel: '',
                rfcReleaseModel: '',
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
                rfcVersionModel: '',
            }
        },
        methods: {
            updateGroupModel: function(data) {
                this.groupModel = data;

                //Update up stream
                this.updateValues('groupModel',data);
            },
            updateValues: function(modelName,modelValue) {
                this.$emit('update_values',{
                    'modelName': modelName,
                    'modelValue': modelValue,
                });
            },
        },
        watch: {
            rfcChangeLead: function() {
                this.updateValues('rfcChangeLead',this.rfcChangeLead);
            },
            rfcImplementationStartModel: function() {
                this.updateValues('rfcImplementationStartModel',this.rfcImplementationStartModel);
            },
            rfcImplementationEndModel: function() {
                this.updateValues('rfcImplementationEndModel',this.rfcImplementationEndModel);
            },
            rfcReleaseModel: function() {
                this.updateValues('rfcReleaseModel',this.rfcReleaseModel);
            },
            rfcStatus: function() {
                this.updateValues('rfcStatus',this.rfcStatus);
            },
            rfcType: function() {
                this.updateValues('rfcType',this.rfcType);
            },
            rfcTypeModel: function() {
                this.updateValues('rfcTypeModel',this.rfcTypeModel);
            },
            rfcVersionModel: function() {
                this.updateValues('rfcVersionModel',this.rfcVersionModel);
            },
        }
    }
</script>

<style scoped>

</style>