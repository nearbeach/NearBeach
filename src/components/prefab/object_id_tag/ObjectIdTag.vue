<script setup lang="ts">
import shortObjectType from '@/utils/dictionary/ShortObjectDictionary.ts';

// PROPS
const props = defineProps({
    id: {
        type: Number,
        required: true,
    },
    objectType: {
        required: true,
        type: String,
        validator: function (value: string): boolean {
            return shortObjectType[value] !== undefined;
        },
    },
});
</script>

<template>
    <span :class="`object-id-tag ${props.objectType}`">
        <RouterLink :to="`${props.objectType}/${props.id}`">
            {{ shortObjectType[props.objectType] }}-{{ props.id }}
        </RouterLink>
    </span>
</template>

<style scoped>
.object-id-tag {
    > a {
        margin-bottom: 0.125rem;
        font-size: 0.75rem;
        text-decoration-line: none;
        color: var(--color-text);
    }
}
</style>
