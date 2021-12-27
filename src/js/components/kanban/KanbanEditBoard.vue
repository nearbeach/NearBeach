<template>
    <div class="card">
        <div class="card-body">
            <h1>{{kanbanBoardResults[0]['fields']['kanban_board_name']}}</h1>
            <hr>

            <!-- Properties for the drag and drop coloumns/levels -->
            <div class="row">
                <div class="col-md-4">
                    <h2>Columns & Levels</h2>
                    <p class="text-instructions">
                        Drag the cards around to sort out the columns how you want them.
                    </p>
                </div>
                <div class="col-md-4">
                    <kanban-property-order v-bind:property-name="'Column'"
                                           v-bind:property-list="columnModel"
                                           v-bind:source="'columnModel'"
                                           v-bind:is-dirty="$v.columnModel.$dirty"
                                           v-bind:is-new-mode="false"
                                           v-bind:kanban-board-id="kanbanBoardResults[0]['pk']"
                                           v-on:update_property_list="updatePropertyList($event)"
                    ></kanban-property-order>
                </div>
                <div class="col-md-4">
                    <kanban-property-order v-bind:property-name="'Level'"
                                           v-bind:property-list="levelModel"
                                           v-bind:source="'levelModel'"
                                           v-bind:is-dirty="$v.columnModel.$dirty"
                                           v-bind:is-new-mode="false"
                                           v-bind:kanban-board-id="kanbanBoardResults[0]['pk']"
                                           v-on:update_property_list="updatePropertyList($event)"
                    ></kanban-property-order>
                </div>
            </div>


            <!-- SAVE -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <button class="btn btn-danger"
                            v-on:click="closeKanban"
                    >
                        Close Kanban Board
                    </button>
                    <button class="btn btn-primary save-changes"
                            v-on:click="backToBoard"
                    >
                        Back to Kanban Board
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    // Validation
    import { required } from 'vuelidate/lib/validators';

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";
    import searchMixin from "../../mixins/searchMixin";

    export default {
        name: "KanbanEditBoard",
        props: {
            columnResults: Array,
            kanbanBoardResults: Array,
            levelResults: Array,
            rootUrl: {
                type: String,
                default: "/",
            },
        },
        mixins: [
            errorModalMixin,
            searchMixin,
        ],
        data() {
            return {
                columnModel: [],
                levelModel: [],
            }
        },
        validations: {
                columnModel: {
                    required,
                },
                levelModel: {
                    required,
                },
        },
        methods: {
            backToBoard: function() {
                window.location.href = `${this.rootUrl}kanban_information/${this.kanbanBoardResults[0]['pk']}/`
            },
            closeKanban: function() {
                axios.post(
                    `${this.rootUrl}kanban_information/${this.kanbanBoardResults[0]['pk']}/close_board/`
                ).then(response => {
                    window.location.href = "/";
                }).catch(error => {
                    this.showErrorModal(error, this.destination);
                })
            },
            updatePropertyList: function(data) {
                this[data['source']] = data['data'];
            },
        },
        mounted() {
            //Send the rootURL to the vuex
            this.$store.commit({
                type: 'updateUrl',
                rootUrl: this.rootUrl,
            })

            //Map the variables into a useable format
            this.columnModel = this.columnResults.map(row => {
                return {
                    'id': row['pk'],
                    'title': row['fields']['kanban_column_name'], 
                };
            });

            this.levelModel = this.levelResults.map(row => {
                return {
                    'id': row['pk'],
                    'title': row['fields']['kanban_level_name'],
                };
            });
        }
    }
</script>

<style scoped>

</style>
