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
                        height: 300,
                        menubar: false,
                        plugins: 'lists',
                        toolbar: [
                           'undo redo | formatselect | alignleft aligncenter alignright alignjustify',
                           'bold italic strikethrough underline backcolor | ' +
                           'bullist numlist outdent indent | removeformat'
                        ]}"
                    v-bind:content_css="false"
                    v-bind:skin="false"
                    v-model="cardDescription"
                />
            </div>
        </div>
        <hr>

        <div class="row">
            <div class="col-md-12">
                <button class="btn btn-secondary"
                        v-on:click="closeModal"
                >
                    Close Modal
                </button>
                <button class="btn btn-primary save-changes"
                        v-on:click="updateCard"
                >
                    Update Card
                </button>
            </div>
        </div>
    </div>
</template>

<script>
    import {mapFields} from 'vuex-map-fields';
    const axios = require('axios');

    export default {
        name: 'CardDescription',
        props: {},
        data() {
            return {}
        },
        computed: {
            ...mapFields([
                'cardDescription',
            ])
        },
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
