<script setup lang="ts">
import { Ellipsis } from 'lucide-vue-next';

const props = defineProps({
    count: {
        type: Number,
        default: 1,
    },
});
</script>

<template>
    <li v-for="index in props.count" :key="index" class="skeleton">
        <div class="skeleton--loader-circle">
            <Ellipsis :size="18" />
        </div>
    </li>
</template>

<style scoped>
.skeleton {
    animation: skeleton-loading 1s linear infinite alternate;
    display: flex;
    flex-direction: row;
    border: 1px solid lightgray;
    margin-bottom: 10px;
    border-radius: 5px;
    align-items: center;
    justify-content: center;
}

@keyframes skeleton-loading {
    0% {
        background-color: rgb(255, 255, 255);
    }
    100% {
        background-color: rgb(250, 250, 250);
    }
}

.skeleton--loader-circle {
    animation: skeleton--loader-circle-loading 1s linear infinite alternate;
    color: grey;
    padding: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

@keyframes skeleton--loader-circle-loading {
    0% {
        color: rgb(89, 123, 237);
    }
    100% {
        color: rgb(169, 30, 237);
    }
}
</style>
