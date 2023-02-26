<template>
    <div class="kanban-container" v-on:scroll="scrollProcedure">
        <!-- Render out the header -->
        <div class="kanban-header-row">
            <div class="kanban-column-header"
                 v-for="column in columnResults"
                 :key="column.pk"
            >
                {{column.fields.kanban_column_name}}
            </div>
        </div>

        <!-- Render out the STICKY header -->
        <div class="kanban-header-row kanban-sticky-row" style="display: none;">
            <div class="kanban-column-header"
                 v-for="column in columnResults"
                 :key="column.pk"
            >
                {{column.fields.kanban_column_name}}
            </div>
        </div>

        <!-- Render each row -->
        <div v-for="level in levelResults"
             :key="level.pk"
        >
            <!-- CREATE THE LEVEL HEADER -->
            <div class="kanban-level-header">
                <div class="kanban-level-div"
                >{{level.fields.kanban_level_name}}</div>
            </div>

            <!-- RENDER THE CELLS -->
            <kanban-row v-bind:level-id="level.pk"
                        v-bind:new-card-info="newCardInfo"
                        v-on:double_clicked_card="doubleClickedCard($event)"
            ></kanban-row>
        </div>

    </div>
</template>

<script>
    //Mixins
    import iconMixin from "../../mixins/iconMixin";
    import KanbanRow from "./KanbanRow.vue";

    //VueX
    import { mapGetters } from "vuex";

    export default {
        name: "KanbanBoard",
        components: {
            KanbanRow,
        },
        props: {
            kanbanBoardResults: {
                type: Array,
                default: () => {
                    return [];
                },
            },
            newCardInfo: {
                type: Array,
                default: () => {
                    return [];
                },
            },
        },
        computed: {
            ...mapGetters({
                columnResults: "getColumnResults",
                levelResults: "getLevelResults",
            })
        },
        mixins: [
            iconMixin,
        ],
        data() {
            return {}
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
                    kanban_sticky.style.display = "none";
                } else {
                    kanban_sticky.style.display = "";
                }
            },
        },
        mounted() {
            //Check the resize procedure
            this.resizeProcedure();

            this.$store.commit({
                type: 'updateKanbanStatus',
                kanbanStatus: this.kanbanBoardResults[0].fields.kanban_board_status,
            })
        },
    }
</script>

<style scoped>

</style>
