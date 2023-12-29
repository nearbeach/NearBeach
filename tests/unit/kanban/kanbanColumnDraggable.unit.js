// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanColumnDraggable from "/src/js/components/kanban/KanbanColumnDraggable.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('KanbanColumnDraggable.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanColumnDraggable, {
        props: {},
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
});