<template>
    <div class="row">
        <div class="col-md-4">
            <h2>Stakeholder Organisation</h2>
            <p class="text-instructions">
                Please search for your stakeholder's organisation in the dropdown box. Once found, please select.
            </p>
            <p class="text-instructions">
              If you can not find your organisation, please
              <a href="javascript:void(0)"
                 v-on:click="openNewOrganisationModal"
              >
                click here to create it.
              </a>
            </p>
        </div>
        <div class="col-md-8">
            <div class="form-group">
                <label>Stakeholder Organisation
                    <span class="error" v-if="!v$.stakeholderModel.required && isDirty"> Please search for a Stakeholder.</span>
                </label>
                <v-select :options="stakeholderFixList"
                          @search="fetchOptions"
                          v-model="stakeholderModel"
                          label="organisation_name"
                          class="get-stakeholders"
                />
            </div>
        </div>

        <!-- MODAL -->
        <new-organisation-modal v-on:created_new_organisation="createdNewOrganisation($event)"
        ></new-organisation-modal>
    </div>
</template>

<script>
    //JavaScript Libraries
    const axios = require('axios');
    import { Modal } from 'bootstrap';

    //VueX
    import { mapGetters} from 'vuex';

    //Validation
    import useVuelidate from '@vuelidate/core'
    import { required } from '@vuelidate/validators'

    //Mixins
    import searchMixin from "../../mixins/searchMixin";

    export default {
        name: "GetStakeholders",
        setup() {
            return { v$: useVuelidate(), }
        },
        components: {
            axios,
            bootstrap,
        },
        mixins: [
            searchMixin
        ],
        props: {
            isDirty: { //Passes the value from the template above where the checking is done
                type: Boolean,
                default: false,
            }
        },
        data() {
            return {
                searchTimeout: '',
                stakeholderFixList: [],
                stakeholderModel: '',
            }
        },
        validations: {
            stakeholderModel: {
                required
            },
        },
        computed: {
            ...mapGetters({
                rootUrl: "getRootUrl",
            }),
        },
        methods: {
            createdNewOrganisation: function(data) {
                //We have recieved a new organisation that the user has created.
                //Place them into the model
                this.stakeholderModel = data;

                //Close the modal
                document.getElementById("newOrganisationModalCloseButton").click();
            },
            fetchOptions: function(search, loading) {
                this.searchTrigger({
                   'return_function': this.getOrganisationData,
                   'searchTimeout': this.searchTimeout,
                   'search': search,
                   'loading': loading,
                });
            },
            getOrganisationData: function(search,loading) {
                // Save the seach data in FormData
                const data_to_send = new FormData();
                data_to_send.set('search',search);

                // Now that the timer has run out, lets use AJAX to get the organisations.
                axios.post(
                    `${this.rootUrl}search/organisation/data/`,
                    data_to_send
                ).then(response => {
                    //Clear the stakeholderFixList
                    this.stakeholderFixList = [];

                    //Extract the required JSON data
                    var extracted_data = response['data'];

                    //Look through the extracted data - and map the required fields into stakeholder fix list
                    extracted_data.forEach((row) => {
                        //Create the creation object
                        var creation_object = {
                            'value': row['pk'],
                            'organisation_name': row['fields']['organisation_name'],
                            'organisation_website': row['fields']['organisation_website'],
                            'organisation_email': row['fields']['organisation_email'],
                            'organisation_profile_picture': row['fields']['organisation_profile_picture'],
                        };

                        //Push that object into the stakeholders
                        this.stakeholderFixList.push(creation_object)
                    });
                }).catch(function (error) {
                    // Get the error modal
                    var elem_cont = document.getElementById("errorModalContent");

                    // Update the content
                    elem_cont.innerHTML = `<strong>Search Organisation Issue:</strong><br/>${error}`;

                    // Show the modal
                    var errorModal = new bootstrap.Modal(document.getElementById('errorModal'), {
                      keyboard: false
                    })
                    errorModal.show();

                    // Hide the loader
                    var loader_element = document.getElementById("loader");
                    loader_element.style.display = "none";
                });
            },
            openNewOrganisationModal: function() {
                var newModal = new Modal(document.getElementById('newOrganisationModal'));

                newModal.show();
                // var newModal = new bootstrap.Modal(
                //     document.getElementById("newOrganisationModal"), {
                //         keyboard: false
                //     })
                // newModal.show();
            },
        },
        watch: {
            stakeholderModel: function() {
                //Send the changes upstream
                this.$emit('update_stakeholder_model',this.stakeholderModel);
            }
        },
        mounted() {
            //Wait 200ms
            setTimeout(() => {
                //Get a default list when mounted
                this.getOrganisationData('','');
            }, 200);
        }
    }
</script>

<style scoped>

</style>