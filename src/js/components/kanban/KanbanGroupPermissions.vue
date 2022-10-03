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
    import GroupsAndUsersModule from "../modules/sub_modules/GroupsAndUsersModule.vue";

    export default {
        name: "KanbanGroupPermissions",
        components: {
            GroupsAndUsersModule,
        },
        props: {
            locationId: {
                type: Number,
                default: 0,
            },
        }
    }
</script>
