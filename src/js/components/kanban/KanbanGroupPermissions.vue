<template>
    <div class="card kanban-group-permissions">
        <div class="card-body">
            <!-- Group Permissions -->
            <groups-and-users-module v-bind:location-id="locationId"
                                     v-bind:destination="'kanban_board'"
            ></groups-and-users-module>
        </div>
    </div>
</template>

<script>
    export default {
        name: "KanbanGroupPermissions",
        props: {
            locationId: Number,
        }
    }
</script>
