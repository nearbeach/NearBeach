<template>
    <div class="card">
        <div class="card-body">
            <h2>Open Kanban Boards</h2>
            <hr>

            <!-- List all kanban boards -->
            
        </div>
    </div>
</template>

<script>
  export default {
      name: "DashboardKanbanList",
      props: {
          kanbanResults: {
            type: Array,
            default: function() {
                return [];
            },
          },
      },
  }
</script>

<style scoped>

</style>