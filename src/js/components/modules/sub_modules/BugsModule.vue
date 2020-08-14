<template>
    <div>
        <h2><i data-feather="x-octagon"></i> Bugs List</h2>
        <p class="text-instructions">
            The following is a list of bugs associated with this {{description}}
        </p>

        <!-- TABLE OF BUGS -->
        <div v-if="bugList.length == 0"
             class="spacer"
        >
            <div class="alert alert-dark">Sorry - there are no bugs associated with this {{description}}</div>
        </div>
        <div v-else>
            <table>
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
                                    Bug No. {{bug['bug_code']}}
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
    </div>
</template>

<script>
    //JavaScript components
    const axios = require('axios');

    export default {
        name: "BugsModule",
        props: [
            'description',
            'location_id',
        ],
        data() {
            return {
                bugList: [],
            }
        },
        methods: {
            getBugHyperLink: function(bug) {
                if (bug['bug_client__list_of_bug_client'] == 'Bugzilla') {
                    return `${bug['bug_client__bug_client_url']}/show_bug.cgi?id=${bug['bug_code']}`;
                }
                return 'javascript:void(0)';
            },
            updateBugList: function() {
                axios.post('')
            },
        }
    }
</script>

<style scoped>

</style>