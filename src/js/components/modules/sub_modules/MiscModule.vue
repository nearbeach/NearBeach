<template>
    <div>
        <list-tags-module v-bind:destination="destination"
                          v-bind:location-id="locationId"
        ></list-tags-module>
    </div>
</template>

<script>
    // JavaScript Libraries
    import {Modal} from "bootstrap";
    import errorModalMixin from "../../../mixins/errorModalMixin";
    import iconMixin from "../../../mixins/iconMixin";
    const axios = require('axios');

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "MiscModule",
        components: {},
        props: [
            'destination',
            'locationId',
        ],
        mixins: [
            errorModalMixin,
            iconMixin,
        ],
        computed: {
            ...mapGetters({
                userLevel: "getUserLevel",
            }),
        },
        data() {
            return {
                noteHistoryResults: [],
            };
        },
        methods: {
            createNewNote: function() {
                var newNoteModal = new Modal(document.getElementById('newNoteModal'));
                    newNoteModal.show();
            },
            getNoteHistoryResults: function() {
                axios.post(
                    `/object_data/${this.destination}/${this.locationId}/note_list/`,
                ).then(response => {
                    this.noteHistoryResults = response['data'];
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updateNoteHistoryResults: function(data) {
                //Add the extra data
                this.noteHistoryResults.push(data[0]);
            }
        },
        mounted() {
            this.getNoteHistoryResults();
        }

    }
</script>

<style scoped>

</style>
