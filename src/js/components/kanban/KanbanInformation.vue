<template>
    <div>
        <div class="container">
            <div class="card">
                <div class="card-body">
                    <h1>Kanban Information</h1>
                    <hr>
                    <div class="row">
                        <!-- Instructions -->
                        <div class="col-md-4">
                            <strong>Instructions</strong>
                            <p class="text-instructions">
                                To add a new card to the board - please click on "New Card". You can link a card to an
                                existing object like a project or task by clicking on "Link Existing Object".
                            </p>
                            <p class="text-instructions">
                                You can drag and drop cards.
                            </p>
                        </div>

                        <!-- Add cards -->
                        <div class="col-md-8">
                            <h2 v-html="kanbanBoardResults[0]['fields']['kanban_board_name']"></h2><br/>
                            <div class="kanban-link">New Card</div>
                            <div class="kanban-link">Link Existing Object</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <hr>

        <!-- Rendering the Kanban Container -->
        <div class="kanban-container">
            <!-- Render out the header -->
            <div class="kanban-row">
                <div class="kanban-column-header"
                     v-for="column in columnResults"
                >
                    {{column['fields']['kanban_column_name']}}
                </div>
            </div>


            <!-- Loop through each level to create the required cards -->
            <div v-for="level in levelResults"
                 v-model="kanbanModel"
            >
                <div class="kanban-row">
                    <div class="kanban-level-header"
                         v-html="level['fields']['kanban_level_name']"
                    ></div>
                </div>


                <!-- Loop through each column to add in the cells -->
                <div class="kanban-row">
<!--                    <transition-group type="transition" :name="'flip-list'">-->
<!--                        <div class="kanban-cell"-->
<!--                             v-for="column in columnResults"-->
<!--                             :key="column['pk']"-->
<!--                        >-->
<!--                            <div class="kanban-card"-->
<!--                                 v-for="card in getCards(column['pk'],level['pk'])"-->
<!--                            >-->
<!--                                {{card['fields']['kanban_card_text']}}-->
<!--                            </div>-->
<!--                        </div>-->
<!--                    </transition-group>-->
                    <div class="kanban-cell"
                         v-for="column in columnResults"
                    >
                        <draggable v-model="kanbanCardResults">
                            <div class="list-group-item"
                                v-for="card in getCards(column['pk'],level['pk'])"
                                v-bind:key="card['pk']"
                            >
                                {{card['fields']['kanban_card_text']}}
                            </div>
                        </draggable>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "KanbanInformation",
        props: {
            columnResults: Array,
            kanbanBoardResults: Array,
            kanbanCardResults: Array,
            levelResults: Array,
        },
        data() {
            return {
                kanbanModel: {}, //Stores the data here temporarily
            }
        },
        methods: {
            getCards(column_id,level_id) {
                //Use the inputs to filter for those cards
                return this.kanbanCardResults.filter(row => {
                    return row['fields']['kanban_column'] == column_id &&
                            row['fields']['kanban_level'] == level_id;
                });
            },
        },
        mounted() {
            /* When the kanban board mounts - we need to setup the kanbanModel. The kanbanModel will store all the lists
             * where the cards are kept.
             *
             * Method
             * ~~~~~~
             * 1. Loop through the columns
             * 2. Inside loop, create the object for that column. Then loop through each level
             * 3. Inside the level - create that level and insert all the cards associated with that model
             */
            this.columnResults.forEach(column_row => {
                //Make sure there is a blank object for this column id
                this.kanbanModel[column_row['pk']] = {};

                //Loop through each level and add the data in
                this.levelResults.forEach(level_row => {
                    //Insert the filtered data for this object location
                    this.kanbanModel[column_row['pk']][level_row['pk']] = this.getCards(column_row['pk'],level_row['pk']);
                });
            });

        }
    }
</script>

<style scoped>

</style>