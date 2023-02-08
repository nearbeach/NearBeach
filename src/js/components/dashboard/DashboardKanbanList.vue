<template>
    <div class="card"
         v-if="kanbanList.length > 0"
    >
        <div class="card-body">
            <h1>Open Kanban Boards</h1>
            <hr>

            <!-- List all kanban boards -->
            <render-object-table v-bind:search-results="kanbanList"
                        v-bind:import-variables="kanbanVariables"
                        v-bind:destination="'kanban'"
                        v-bind:root-url="rootUrl"
            ></render-object-table>
        </div>
    </div>
</template>

<script>
    const axios = require("axios");

    //Mixins
    import errorModalMixin from "../../mixins/errorModalMixin";

    //Components
    import RenderObjectTable from "../render/RenderObjectTable.vue";

    export default {
        name: "DashboardKanbanList",
        components: {
            RenderObjectTable,
        },
        props: {
            rootUrl: {
                type: String,
                default: "/",
            },
        },
        data: () => ({
            kanbanList: [],
            kanbanVariables: {
                header: 'Kanban Boards',
                prefix: 'Kan',
                id: 'id',
                title: 'title',
                status: 'status',
                end_date: 'end_date',
            },
        }),
        mixins: [
            errorModalMixin,
        ],
        methods: {
            getMyKanbanList: function() {
                //Use axios to get data
                axios.post(
                    `${this.rootUrl}dashboard/get/kanban_list/`
                ).then((response) => {
                    //Map out the data to a flatted table for rendering purposes.
                    this.kanbanList = response.data.map(row => {
                        return {
                            id : row.pk,
                            title: row.fields.kanban_board_name,
                            status: "Open",
                            end_date: "",
                        }
                    });
                }).catch((error) => {
                    this.showErrorModal(error, "Kanban List", 0);
                });
            }
        },
        mounted() {
            //Get list of kanban items
            this.getMyKanbanList();
        }
        
    }
</script>

<style scoped>

</style>