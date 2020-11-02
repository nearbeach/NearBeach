<template>
    <div class="kanban-container">
        <!-- Render out the header -->
        <div class="kanban-row">
            <div class="kanban-column-header"
                 v-for="column in columnResults"
            >
                {{column['fields']['kanban_column_name']}}
            </div>
        </div>

        <!-- Render each row -->
        <div v-for="level in levelResults">
            <!-- CREATE THE LEVEL HEADER -->
            <div class="kanban-level-header">{{level['fields']['kanban_level_name']}}</div>

            <!-- RENDER THE CELLS -->
            <kanban-row v-bind:kanban-row-model="kanbanModel[level['pk']]"
                        v-bind:column-results="columnResults"
                        v-bind:level-id="level['pk']"
            ></kanban-row>
        </div>

    </div>
</template>

<script>
    export default {
        name: "KanbanBoard",
        props: {
            columnResults: Array,
            kanbanBoardResults: Array,
            kanbanCardResults: Array,
            levelResults: Array,
        },
        data() {
            return {
                kanbanModel: {}, //Stores the data here temporarily
                list1: [{'id':1,'name':'The fart copter'}],
                list2: [{'id':2,'name':'The fart copter'}],
            }
        },
        methods: {
            getCards: function(level_id,column_id) {
                //Use the inputs to filter for those cards
                var return_data = this.kanbanCardResults.filter(row => {
                    return row['fields']['kanban_column'] == column_id &&
                            row['fields']['kanban_level'] == level_id;
                });
                return return_data;
            },
        },
        mounted() {
            /* When the kanban board mounts - we need to setup the kanbanModel. The kanbanModel will store all the lists
             * where the cards are kept.
             *
             * Method
             * ~~~~~~
             * 1. Loop through the level
             * 2. Inside loop, create the object for that level. Then loop through each column
             * 3. Inside the column - create that column and insert all the cards associated with that model
             */
            var temp_object = {}

            this.levelResults.forEach(level_row => {
                //Make sure there is a blank object for this level id
                temp_object[level_row['pk']] = {};

                //Loop through each level and add the data in
                this.columnResults.forEach(column_row => {
                    //Insert the filtered data for this object location
                    temp_object[level_row['pk']][column_row['pk']] = this.getCards(level_row['pk'],column_row['pk']);
                });
            });

            //Send the data to the kanban model
            this.kanbanModel = temp_object;
        },
    }
</script>

<style scoped>

</style>