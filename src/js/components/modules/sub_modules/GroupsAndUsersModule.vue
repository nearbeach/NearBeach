<template>
    <div>
        <h2><i data-feather="grid"></i> Groups and Users</h2>
        <p class="text-instructions">
            The following list are all the Groups connected to this {{destination}}
        </p>
    </div>
</template>

<script>
    export default {
        name: "GroupsAndUsersModule",
        props: [
            'destination',
            'location_id',
        ]
    }
</script>

<style scoped>

</style>