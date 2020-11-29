<template>
    <div>
        <h2><i data-feather="link"></i> {{destination}} Links</h2>
        <p class="text-instructions">
            The following are links to other objects like projects/tasks/requirements. You can link a {{destination}}
            to these other objects to symbolise a connection between the two.
        </p>

        <!-- REQUIREMENT LINKS -->
        <div v-if="linkResults.length == 0"
             class="requirement-item-spacer"
        >
            <div class="alert alert-dark">Sorry - there are no Links for this requirement.</div>
        </div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <td width="75%">Object Description</td>
                        <td width="25%">Status</td>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="link in linkResults">
                        <td v-html="extractObjectDescription(link)"></td>
                        <td>{{extractObjectStatus(link)}}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    export default {
        name: "ObjectLinks",
        props: {
            destination: String,
            location_id: Number,
        },
        data() {
            return {
                linkResults: [],
            }
        },
        methods: {
            extractObjectDescription: function(link) {
                return "NEED TO PROGRAM";
            },
            extractObjectStatus: function(link) {
                return "NEED TO PROGRAM";
            },
            updateLinkResults: function() {
                //Get the data from the database
                axios.post(
                    `/object_data/${this.destination}/${this.location_id}/object_link_list/`,
                ).then((response) => {
                    this.linkResults = response['data'];
                });
            },
        },
        mounted() {
            //Get data
            this.updateLinkResults();
        }

    }
</script>

<style scoped>

</style>