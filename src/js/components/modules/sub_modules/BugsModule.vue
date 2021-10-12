<template>
    <div>
        <h2><IconifyIcon v-bind:icon="icons.bugIcon"></IconifyIcon> Bugs List</h2>
        <p class="text-instructions">
            The following is a list of bugs associated with this {{destination}}
        </p>

        <!-- TABLE OF BUGS -->
        <div v-if="bugList.length === 0"
             class="spacer"
        >
            <div class="alert alert-dark">Sorry - there are no bugs associated with this {{destination}}</div>
        </div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <td>Bug Description</td>
                        <td>Status</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="bug in bugList">
                        <td>
                            <a v-bind:href="getBugHyperLink(bug)" target="_blank">
                                <p>
                                    {{bug['bug_description']}}
                                </p>
                                <div class="spacer"></div>
                                <p class="small-text">
                                    Bug No. {{bug['bug_code']}} - {{bug['bug_client__bug_client_name']}}
                                </p>
                            </a>
                        </td>
                        <td>
                            {{bug['bug_status']}}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Add Bug Button -->
        <!-- TO DO - limit it to certain users -->
        <hr>
        <div class="row submit-row">
            <div class="col-md-12">
                <button class="btn btn-primary save-changes"
                        v-on:click="addNewBug"
                >
                    Add Bug
                </button>
            </div>
        </div>

        <!-- Modals -->
        <add-bug-wizard v-bind:destination="destination"
                        v-bind:location-id="locationId"
                        v-on:append_bug_list="appendBugList($event)"
        ></add-bug-wizard>
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');
    import {Modal} from "bootstrap";

    //Mixins
    import errorModalMixin from '../../../mixins/errorModalMixin';
    import iconMixin from "../../../mixins/iconMixin";

    export default {
        name: "BugsModule",
        props: [
            'destination',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        data() {
            return {
                bugList: [],
            }
        },
        methods: {
            addNewBug: function() {
                var addBugModal = new Modal(document.getElementById('addBugModal'));
                    addBugModal.show();
            },
            appendBugList: function(data) {
                //Append the data
                this.bugList.push(data[0]['fields']);
            },
            getBugHyperLink: function(bug) {
                
                if (bug['bug_client__list_of_bug_client__bug_client_name'] == 'Bugzilla') {
                    return `${bug['bug_client__bug_client_url']}/show_bug.cgi?id=${bug['bug_code']}`;
                }
                return 'javascript:void(0)';
            },
            getBugList: function() {
                //We don't need to get the bug list when destination is requirement_items
                if (this.destination === 'requirement_item') {
                    //Jet pack out of there
                    return;
                }

                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/bug_list/`
                ).then((response) => {
                    //Clear the current list
                    this.bugList = [];

                    //Loop through the results, and push each rows into the array
                    response['data'].forEach((row) => {
                        this.bugList.push(row);
                    });
                }).catch((error) => {
                    this.showErrorModal(error, this.destination);
                })
            },
        },
        mounted() {
            this.getBugList();
        }
    }
</script>

<style scoped>

</style>
