<script setup lang="ts">
import { computed } from 'vue';

// PROPS
const props = defineProps({
    higherOrderStatus: {
        required: true,
        type: String,
        validator: function (value: string): boolean {
            return ['backlog', 'blocked', 'normal', 'closed'].includes(
                value.toLowerCase()
            );
        },
    },
    status: {
        type: String,
        required: true,
    },
});

// COMPUTED
const classNames = computed(() => {
    return `object-status-tag ${props.higherOrderStatus}`;
});
</script>

<template>
    <span :class="classNames">
        {{ status }}
    </span>
</template>

<style scoped>
.object-status-tag {
    padding: 0.125rem 0.75rem;
    margin-bottom: 0.125rem;
    border-radius: var(--border-radius);
    font-size: 0.75rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    &.backlog {
        background-color: var(--info);
    }

    &.blocked {
        background-color: var(--danger);
    }

    &.normal {
        background-color: var(--primary);
    }

    &.closed {
        background-color: var(--success);
    }
}
</style>
