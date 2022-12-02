<template>
    <div>
        <div class="row">
            <div class="col-md-4">
                <strong>Card Description</strong>
                <p class="text-instructions">
                    Fill out a detailed description for the card, then click on the "Update Card" button
                    to update the card.
                </p>
            </div>
            <div class="col-md-8">
                <editor
                    :init="{
                        file_picker_types: 'image',
                        height: 300,
                        images_upload_handler: uploadImage,
                        menubar: false,
                        paste_data_images: true,
                        plugins: ['lists','paste','table'],
                        toolbar: [
                           'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                           'bold italic strikethrough underline backcolor | table | ' +
                           'bullist numlist outdent indent | removeformat'
                        ]}"
                    v-bind:content_css="false"
                    v-bind:skin="false"
                    v-model="cardDescription"
                    v-bind:disabled="kanbanStatus === 'Closed'"
                />
            </div>
        </div>
        <hr>

        <div class="row">
            <div class="col-md-12">
                <button class="btn btn-secondary"
                        v-on:click="closeModal"
                >
                    Close
                </button>
                <button class="btn btn-primary save-changes"
                        v-on:click="updateCard"
                        v-if="kanbanStatus !== 'Closed'"
                >
                    Update Card
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    //Axios
    const axios = require('axios');

    //TinyMce
    import Editor from '@tinymce/tinymce-vue'

    //VueX
    import { mapGetters } from 'vuex';

    //Mixins
    import uploadMixin from "../../mixins/uploadMixin";

    export default {
        name: 'CardDescription',
        components: {
            'editor': Editor,
        },
        props: {},
        data() {
            return {}
        },
        computed: {
            ...mapGetters({
                kanbanStatus: 'getKanbanStatus',
            }),
            cardDescription: {
                get () {
                    return this.$store.state.card.cardDescription;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'cardDescription',
                        value: value,
                    });
                },
            },
        },
        mixins: [
            uploadMixin,
        ],
        methods: {
            closeModal: function() {
                document.getElementById("cardInformationModalCloseButton").click();
            },
            updateCard: function() {
                this.$emit('update_card');
            },
        },
    }
</script>
