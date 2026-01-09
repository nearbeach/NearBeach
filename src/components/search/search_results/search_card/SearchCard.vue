<script setup lang="ts">
import ObjectIdTag from '@/components/prefab/object_id_tag/ObjectIdTag.vue';
import ObjectStatusTag from '@/components/prefab/object_status_tag/ObjectStatusTag.vue';
import shortObjectType from '@/utils/dictionary/ShortObjectDictionary.ts';

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
    status: {
        type: String,
        required: false,
        default: '',
    },
    title: {
        type: String,
        required: true,
    },
});
</script>

<template>
    <div class="search-card">
        <ObjectIdTag :id="props.id" :object-type="props.objectType" />
        <div class="object-title">
            <RouterLink :to="`${props.objectType}/${props.id}`">{{
                title
            }}</RouterLink>
        </div>
        <ObjectStatusTag
            :higher-order-status="higherOrderStatus"
            :status="props.status"
        />
    </div>
</template>

<style scoped>
.search-card {
    display: grid;
    padding: 0.5rem;
    border-bottom: var(--border-muted) var(--border-style) var(--border-width);
    grid-template-columns: repeat(3, minmax(0, 1fr));
    grid-template-rows: 1.5rem 1fr;

    @media (--medium-screen) {
        grid-template-columns: repeat(6, minmax(0, 1fr));
    }

    .object-id-tag {
        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 1;
        grid-row-end: 2;
    }

    .object-title {
        grid-column-start: 1;
        grid-column-end: 4;
        grid-row-start: 2;
        grid-row-end: 3;

        @media (--medium-screen) {
            grid-column-end: 6;
        }
    }

    .object-status-tag {
        grid-column-start: 3;
        grid-column-end: 4;
        grid-row-start: 1;
        grid-row-end: 2;

        @media (--medium-screen) {
            grid-column-start: 6;
            grid-column-end: 7;
        }
    }
}
</style>
