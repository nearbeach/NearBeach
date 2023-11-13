// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanRow from "/src/js/components/kanban/KanbanRow.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('KanbanRow.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanRow, {
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