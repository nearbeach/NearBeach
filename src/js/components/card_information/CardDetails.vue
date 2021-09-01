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
                    <div class="col-md-12 mt-4">
                        <label>Card Column</label>
                        <v-select v-bind:options="listColumns"
                                  v-bind:label="'column'"
                                  v-bind:clearable="false"
                                  v-model="cardColumn"
                        ></v-select>
                    </div>

                    <div class="col-md-12 mt-4">
                        <label>Card Level</label>
                        <v-select v-bind:options="listLevels"
                                  v-bind:label="'level'"
                                  v-bind:clearable="false"
                                  v-model="cardLevel"
                        ></v-select>
                    </div>
                </div>
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
    import { mapFields } from 'vuex-map-fields';
    const axios = require('axios');

    export default {
        name: 'CardDetails',
        props: {},
        data() {
            return {
                tempModel: '',
            }
        },
        computed: {
            ...mapFields([
                'cardId',
                'cardTitle',
                'cardColumn',
                'cardLevel',
                'listColumns',
                'listLevels',
            ]),
        },
        methods: {
            closeModal: function() {
                document.getElementById("cardInformationModalCloseButton").click();
            },
            updateCard: function() {
                this.$store.commit({
                    type: 'updateKanbanCard',
                    cardId: this.cardId,
                    cardTitle: this.cardTitle,
                    cardColumn: this.cardColumn,
                    cardLevel: this.cardLevel,
                    listColumns: this.listColumns,
                    listLevels: this.listLevels,
                })

                //TEMP - need to replace with a close functionality
                this.$emit('update_card');
            },
        },
    }
</script>
