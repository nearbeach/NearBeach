<template>
    <div class="kanban-container" v-on:scroll="scrollProcedure">
        <!-- Render out the header -->
        <div class="kanban-header-row">
            <div class="kanban-column-header"
                 v-for="column in columnResults"
            >
                {{column['fields']['kanban_column_name']}}
            </div>
        </div>

        <!-- Render out the STICKY header -->
        <div class="kanban-header-row kanban-sticky-row" style="display: none;">
            <div class="kanban-column-header"
                 v-for="column in columnResults"
            >
                {{column['fields']['kanban_column_name']}}
            </div>
        </div>

        <!-- Render each row -->
        <div v-for="level in levelResults">
            <!-- CREATE THE LEVEL HEADER -->
            <div class="kanban-level-header">
                <div class="kanban-level-div"
                >{{level['fields']['kanban_level_name']}}</div>
            </div>

            <!-- RENDER THE CELLS -->
            <kanban-row v-bind:kanban-row-model="kanbanModel[level['pk']]"
                        v-bind:column-results="columnResults"
                        v-bind:level-id="level['pk']"
                        v-bind:new-card-info="newCardInfo"
                        v-on:double_clicked_card="doubleClickedCard($event)"
            ></kanban-row>
        </div>

    </div>
</template>

<script>
    //Mixins
    import iconMixin from "../../mixins/iconMixin";

    export default {
        name: "KanbanBoard",
        props: {
            columnResults: Array,
            kanbanBoardResults: Array,
            kanbanCardResults: Array,
            levelResults: Array,
            newCardInfo: Array,
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {
                kanbanModel: {}, //Stores the data here temporarily
                list1: [{'id':1,'name':'The fart copter'}],
                list2: [{'id':2,'name':'The fart copter'}],
            }
        },
        created() {
            window.addEventListener("resize", this.resizeProcedure);
            window.addEventListener("scroll", this.scrollProcedure);
        },
        destroyed() {
            window.removeEventListener("resize", this.resizeProcedure);
            window.removeEventListener("scroll", this.scrollProcedure);
        },
        methods: {
            doubleClickedCard: function(data) {
                //Send data upstream
                this.$emit('double_clicked_card',data);
            },
            getCards: function(level_id,column_id) {
                //Use the inputs to filter for those cards
                var return_data = this.kanbanCardResults.filter(row => {
                    return row['fields']['kanban_column'] == column_id &&
                            row['fields']['kanban_level'] == level_id;
                });
                return return_data;
            },
            resizeProcedure: function() {
                // Get the screen size and the columns width
                const columns_width = this.columnResults.length * 400;
                let kanban_container_width = document.getElementsByClassName("kanban-container")
                kanban_container_width = kanban_container_width[0].clientWidth;

                //If the columns width is smaller than the screen size
                // - we will need to adjust the kanban-level-div
                if (columns_width < kanban_container_width) {
                    //Add in the width restrictions
                    var elements = document.getElementsByClassName("kanban-level-div");

                    //Loop through each element
                    Array.from(elements).forEach(element => {
                        element.style = `max-width: ${columns_width}px;`;
                    })
                } else {
                    //Remove the old CSS Styling
                    let elements = document.getElementsByClassName("kanban-level-div");

                    //Loop through each element
                    Array.from(elements).forEach(element => {
                        element.style = `max-width: null;`;
                    })
                }
            },
            scrollProcedure: function() {
                //Make sure the kanban-sticky-row matches the scroll left for the kanban-container
                var kanban_sticky = document.getElementsByClassName("kanban-sticky-row")[0],
                    kanban_container = document.getElementsByClassName("kanban-container")[0];

                kanban_sticky.scrollLeft = kanban_container.scrollLeft;

                //Get the distance to the top of the page
                var scrollTop = (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;

                //Determine if we are hidding the element or not
                if (scrollTop < 90) {
                    kanban_sticky['style']['display'] = "none";
                } else {
                    kanban_sticky['style']['display'] = "";
                }
            },
            updateKanbanModel: function() {
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
            }
        },
        mounted() {
            this.updateKanbanModel();

            //Check the resize procedure
            this.resizeProcedure();
        },
    }
</script>

<style scoped>

</style>
