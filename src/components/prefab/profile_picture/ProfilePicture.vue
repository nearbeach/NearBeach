<script setup lang="ts">
import { computed } from "vue";

// Define props
const props = defineProps({
    name: {
        type: String,
        required: false,
    },
    url: {
        type: [String, null],
        required: true,
    },
})

// Define computed
const altText = computed(() => {
    if (props.name === undefined || props.name === null || props.name === "") {
        return "Profile Picture";
    }

    return `${props.name}'s profile picture`;
})
</script>

<template>
    <div class="profile-picture">
        <div class="no-profile-picture"
             v-if="url === '' || url === null || url === undefined"
        ></div>
        <img v-else
             class="profile-picture"
             :src="url"
             :alt="altText"
        />
    </div>
</template>

<style scoped>
.profile-picture {
    > .no-profile-picture,
    > img {
        width: 100%;
        height: 100%;
    }

    > .no-profile-picture {
        background-color: var(--secondary);
        border-radius: 50%;
    }
}

</style>