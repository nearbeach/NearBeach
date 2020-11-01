<template>
    <draggable class="list-group kanban-cell" group="tasks" :list="masterList" @end="onEnd($event)">
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