<script setup lang="ts">
import CardComponent from '@/components/prefab/card/CardComponent.vue';
import TextInput from '@/components/prefab/text_input/TextInput.vue';
import DatetimeComponent from '@/components/prefab/datetime_component/DatetimeComponent.vue';
import NumberInput from '@/components/prefab/number_input/NumberInput.vue';

// Define Modals
const endDateModel = defineModel('endDateModel', {
    type: Date,
});
const priorityModel = defineModel('priorityModel', {
    type: String,
    default: 'Normal',
});
const startDateModel = defineModel('startDateModel', {
    type: Date,
});
const statusModel = defineModel('statusModel', {
    type: String,
    default: 'In Progress',
});
const storyPointsModel = defineModel('storyPointModel', {
    type: Number,
    default: 0,
});

// Define Data
const fieldValidation: Record<string, boolean> = {
    endDateModel: true,
    priorityModel: true,
    startDateModel: true,
    statusModel: true,
};
</script>

<template>
    <CardComponent class="properties-component">
        <h3>Properties</h3>

        <TextInput
            class="status compact"
            v-model="statusModel"
            label="Status"
            @isValid="(value) => (fieldValidation['statusModel'] = value)"
        />
        <TextInput
            class="priority compact"
            v-model="priorityModel"
            label="Priority"
            @isValid="(value) => (fieldValidation['priorityModel'] = value)"
        />

        <NumberInput
            class="story-points compact"
            v-model="storyPointsModel"
            label="Story Points"
            :min-value="0"
            :max-value="10"
        />

        <DatetimeComponent
            class="start-date compact"
            v-model="startDateModel"
            label="Start Date"
            @isValid="(value) => (fieldValidation['startDateModel'] = value)"
        />
        <DatetimeComponent
            class="end-date compact"
            v-model="endDateModel"
            label="End Date"
            @isValid="(value) => (fieldValidation['endDateModel'] = value)"
        />
    </CardComponent>
</template>

<style scoped>
.properties-component {
    display: grid;
    grid-template-columns: minmax(0, 1fr);
    grid-column-gap: 0.5rem;
	padding: 0 0.5rem;

    @media (--small-screen) {
        grid-template-columns: repeat(6, minmax(0, 1fr));
        grid-template-rows: 2.5rem 1fr 1fr;
    }

	@media (--medium-screen) {
		padding: 0.5rem;
	}

    @media (--large-screen) {
        grid-template-columns: minmax(0, 1fr);
        grid-template-rows: 2.5rem repeat(5, minmax(0, 1fr));
    }

    > h3 {
        margin: 0 0 1.5rem 0;

        @media (--small-screen) {
            grid-column-start: 1;
            grid-column-end: 7;
            grid-row-start: 1;
            grid-row-end: 2;
        }

        @media (--large-screen) {
            grid-column-start: 1;
            grid-column-end: 2;
        }
    }

    > .status {
        @media (--small-screen) {
            grid-column-start: 1;
            grid-column-end: 3;
            grid-row-start: 2;
            grid-row-end: 3;
        }
        @media (--large-screen) {
            grid-column-start: 1;
            grid-column-end: 2;
            grid-row-start: 2;
            grid-row-end: 3;
        }
    }

    > .priority {
        @media (--small-screen) {
            grid-column-start: 3;
            grid-column-end: 5;
            grid-row-start: 2;
            grid-row-end: 3;
        }

        @media (--large-screen) {
            grid-column-start: 1;
            grid-column-end: 2;
            grid-row-start: 3;
            grid-row-end: 4;
        }
    }

    > .story-points {
        @media (--small-screen) {
            grid-column-start: 5;
            grid-column-end: 7;
            grid-row-start: 2;
            grid-row-end: 3;
            grid-row-start: 2;
            grid-row-end: 3;
        }

        @media (--large-screen) {
            grid-column-start: 1;
            grid-column-end: 2;
            grid-row-start: 4;
            grid-row-end: 5;
        }
    }

    > .start-date {
        @media (--small-screen) {
            grid-column-start: 1;
            grid-column-end: 4;
            grid-row-start: 3;
            grid-row-end: 4;
        }
        @media (--large-screen) {
            grid-column-start: 1;
            grid-column-end: 2;
            grid-row-start: 5;
            grid-row-end: 6;
        }
    }

    > .end-date {
        @media (--small-screen) {
            grid-column-start: 4;
            grid-column-end: 7;
            grid-row-start: 3;
            grid-row-end: 4;
        }

        @media (--large-screen) {
            grid-column-start: 1;
            grid-column-end: 2;
            grid-row-start: 6;
            grid-row-end: 7;
        }
    }
}
</style>
