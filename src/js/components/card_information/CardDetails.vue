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
                        <n-select v-bind:options="listColumns"
                                  label="column"
                                  v-model:value="cardColumn"
                        ></n-select>
                    </div>

                    <div class="col-md-12 mt-4">
                        <label>Card Level</label>
                        <n-select v-bind:options="listLevels"
                                  label="level"
                                  v-model:value="cardLevel"
                        ></n-select>
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
    const axios = require('axios');
    import { NSelect } from 'naive-ui';

    export default {
        name: 'CardDetails',
        components: {
            NSelect,
        },
        data() {
            return {
                tempModel: '',
            }
        },
        computed: {
            cardId: {
                get () {
                    return this.$store.cardId;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'cardId',
                        value: value,
                    });
                },
            },
            cardTitle: {
                get () {
                    return this.$store.cardTitle;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'cardTitle',
                        value: value,
                    });
                },
            },
            cardColumn: {
                get () {
                    return this.$store.cardColumn;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'cardColumn',
                        value: value,
                    });
                },
            },
            cardLevel: {
                get () {
                    return this.$store.cardLevel;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'cardLevel',
                        value: value,
                    });
                },
            },
            listColumns: {
                get () {
                    return this.$store.listColumns;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'listColumns',
                        value: value,
                    });
                },
            },
            listLevels: {
                get () {
                    return this.$store.listLevels;
                },
                set (value) {
                    this.$store.commit('updateValue', {
                        field: 'listLevels',
                        value: value,
                    });
                },
            },
        },
        methods: {
            closeModal: function() {
                document.getElementById("cardInformationModalCloseButton").click();
            },
            updateCard: function() {
                this.$store.commit({
                    type: 'updateKanbanCard',
                    card_id: this.cardId,
                    kanban_card_text: this.cardTitle,
                    kanban_column: this.cardColumn,
                    kanban_level: this.cardLevel,
                })

                //TEMP - need to replace with a close functionality
                this.$emit('update_card');
            },
        },
    }
</script>
