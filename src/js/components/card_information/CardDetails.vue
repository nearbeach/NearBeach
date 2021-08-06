<template>
    <div>
        <!-- Card Text -->
        <div class="row">
            <div class="col-md-4">
                <strong>Card Title</strong>
                <p class="text-instructions">
                    Write an appropriate name for the kanban card. To update click on the "Update" button.
                </p>
            </div>
            <div class="col-md-8">
                <label>Card Title</label>
                <input v-model="cardTitle"
                        class="form-control"
                >
            </div>
        </div>
        <hr>

        <!-- CARD LOCATION -->
        <div class="row">
            <div class="col-md-4">
                <strong>Card Location</strong>
                <p class="text-instructions">
                    Select the appropriate location for this card.
                </p>
            </div>

            <div class="col-md-8">
                <div class="row">
                    <div class="col-md-12">
                        <label>Card Column</label>
                        <v-select :options="[{label: 'Canada', code: 'ca'}]"></v-select>
                    </div>

                    <div class="col-md-12">
                        <label>Card Level</label>]
                        <v-select :options="[{label: 'Canada', code: 'ca'}]"></v-select>
                    </div>
                </div>
            </div>
        </div>

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
        <hr>
    </div>
</template>

<script>
    import { mapFields } from 'vuex-map-fields';
    const axios = require('axios');

    export default {
        name: 'CardDetails',
        props: {},
        computed: {
            ...mapFields([
                'cardTitle',
                'listColumns',
                'listLevels',
            ]),
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
