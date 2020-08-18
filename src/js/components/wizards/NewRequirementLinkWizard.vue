<template>
    <div class="modal-body">
        <!-- CHOOSING A OBJECT TYPE -->
        <div class="row">
            <div class="col-md-4">
                <strong>Object Selector</strong>
                <p class="text-instructions">
                    Please select which object you would like to link to this requirement.
                </p>
            </div>
            <div class="col-md-8">
                <v-select :options="objectSelection"
                          v-model="objectModel"
                          class="object-selection"
                          v-if="!isSearching"
                ></v-select>
                <div v-else
                     class="alert alert-success"
                >
                    Searching for {{objectModel}}s
                </div>
            </div>
        </div>
        <hr>

        <!-- SELECTING WHICH OBJECTS TO LINK TO -->
        <div class="row">
            <div class="col-md-4">
                <strong>Select Links</strong>
                <p class="text-instructions">
                    Please select which of the objects you want to connect to this requirement.
                </p>
            </div>
            <div class="col-md-8">
                <div id="link_wizard_results">
                    <img src="/static/NearBeach/images/placeholder/search.svg" alt="Searching..." />
                </div>
            </div>

        </div>
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');

    export default {
        name: "NewRequirementLinkWizard",
        props: [
            'destination',
            'locationId',
        ],
        data() {
            return {
                isSearching: false,
                objectModel: null,
                objectResults: [],
                objectSelection: [
                    'Project',
                    'Task',
                    'Opportunity',
                ],
            }
        },
        watch: {
            objectModel: function() {
                //User has chosen an object.
                if (this.objectModel == null) {
                    //Ok - then removed the objects. We don't need to do anything
                    this.isSearching = false;
                    return;
                }

                //Tell the form that we are searching
                this.isSearching = true;

                //Now to use axios to get the data we require
                axios.post(
                    `/object_data/${this.destination}/%{this.locationId}/${this.objectModel.toLowerCase()}/link_list/`
                ).then(response => {
                    //Load the data into the array
                    this.objectResults = response['data'];

                    //Tell the user we are no longer searching
                    this.isSearching = false;
                }).catch((error) => {
                    console.log("ERROR: ",error);
                })
            }
        }
    }
</script>

<style scoped>

</style>