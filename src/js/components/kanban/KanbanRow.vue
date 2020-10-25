<template>
    <div class="kanban-row">
        <kanban-card v-for="card in columnResults"></kanban-card>
    </div>
</template>

<script>
    export default {
        name: "KanbanRow",
        props: {
            columnResults: Array,
            kanbanRowModel: Array
        }
    }
</script>

<style scoped>

</style>