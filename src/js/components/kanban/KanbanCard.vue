<template>
    <draggable class="list-group kanban-cell"
               group="tasks"
               :list="masterList"
               @end="onEnd($event)"
               v-bind:id="`kanban_cell_${levelId}_${columnId}`"
               v-bind:data-level="levelId"
               v-bind:data-column="columnId"
    >
        <div class="list-group-item"
             v-for="card in masterList"
             :key="card['pk']"
             :id="card['pk']"
        >
            {{card['fields']['kanban_card_text']}}
        </div>
    </draggable>
</template>

<script>
    export default {
        name: "KanbanCard",
        props: {
            columnId: Number,
            levelId: Number,
            masterList: Array,
        },
        methods: {
            onEnd: function(event) {
                console.log("Event: ",event);

            },
        },
    }
</script>

<style scoped>

</style>