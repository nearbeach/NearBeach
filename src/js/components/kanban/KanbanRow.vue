<template>
    <div class="kanban-row">
        <div v-for="card in columnResults">
            <kanban-card v-bind:master-list="getMasterList(card['pk'])"></kanban-card>
        </div>
    </div>
</template>

<script>
    export default {
        name: "KanbanRow",
        props: {
            columnResults: Array,
            kanbanRowModel: Object,
        },
        methods: {
            getMasterList: function(row_id) {
                //Determine if the kanban Row exists - if not defined, send back empty array.
                if (this.kanbanRowModel == undefined) {
                    return [];
                }

                //There exists data -> send it back to the user
                return this.kanbanRowModel[row_id];
            }
        }
    }
</script>

<style scoped>

</style>