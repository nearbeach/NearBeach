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
    import axios from 'axios';
    import ListTagsModule from "./ListTagsModule.vue";

    //VueX
    import { mapGetters } from 'vuex';

    export default {
        name: "MiscModule",
        components: {
            ListTagsModule,
        },
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
                rootUrl: "getRootUrl",
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
                    `${this.rootUrl}object_data/${this.destination}/${this.locationId}/note_list/`,
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
            //Wait 200ms before getting the data
            setTimeout(() => {
                this.getNoteHistoryResults();
            }, 200);
        }
    }
</script>

<style scoped>

</style>
