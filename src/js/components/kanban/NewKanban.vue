<template>
    <div class="card">
        <div class="card-body">
            <h1>New Kanban</h1>
            <hr>

            <div class="row">
                <!-- DESCRIPTION -->
                <div class="col-md-4">
                    <strong>Please note</strong>
                    <p class="text-instructions">
                        Board names must be unique.
                    </p>
                </div>

                <!-- BOARD NAME -->
                <div class="col-md-8">
                    <div class="form-group">
                        <label>Kanban Board Name</label>
                        <input type="text"
                               class="form-control"
                               v-model="kanbanBoardNameModel"
                        >
                    </div>
                </div>
            </div>
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
                    <kanban-property-order v-bind:property-name="'Columns'"
                                           v-bind:property-list="columnModel"
                                           v-bind:source="'columnModel'"
                                           v-on:update_property_list="updatePropertyList($event)"
                    ></kanban-property-order>
                </div>
                <div class="col-md-4">
                    <kanban-property-order v-bind:property-name="'Levels'"
                                           v-bind:property-list="levelModel"
                                           v-bind:source="'levelModel'"
                                           v-on:update_property_list="updatePropertyList($event)"
                    ></kanban-property-order>
                </div>
            </div>

            <!-- SAVE -->
            <hr>
            <div class="row submit-row">
                <div class="col-md-12">
                    <button class="btn btn-primary save-changes"
                            v-on:click="addNewKanban"
                    >
                        Add Kanban
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    const axios = require('axios');

    export default {
        name: "NewKanban",
        props: {},
        data() {
            return {
                columnModel: [{
                    id: 0,
                    title: 'Backlog',
                }, {
                    id: 1,
                    title: 'Blocked',
                }, {
                    id: 2,
                    title: 'In Progress',
                }, {
                    id: 4,
                    title: 'Review and QA',
                }, {
                    id: 5,
                    title: 'Completed',
                },],
                kanbanBoardNameModel: '',
                levelModel: [{
                    id: 0,
                    title: 'Sprint 1',
                }, {
                    id: 1,
                    title: 'Sprint 2',
                },],
            }
        },
        methods: {
            addNewKanban: function() {
                //Create the data_to_send
                const data_to_send = new FormData();
                data_to_send.set('kanban_board_name',this.kanbanBoardNameModel);

                //Loop through all the column models
                this.columnModel.forEach(column => {
                    data_to_send.append('column_title',column['title']);
                });

                this.levelModel.forEach(level => {
                    data_to_send.append('level_title',level['title']);
                });

                //Use axios to send the data
                axios.post(
                    `/new_kanban_save/`,
                    data_to_send
                ).then(response => {
                    console.log("Response: ",response);
                }).catch(error => {
                    console.log("Error: ",error);
                });
            },
            updatePropertyList: function(data) {
                this[data['source']] = data['data'];
            },
        }
    }
</script>

<style scoped>

</style>