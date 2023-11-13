// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanColumn from "/src/js/components/kanban/KanbanColumn.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('KanbanColumn.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanColumn, {
        props: {
            columnId:1,
            columnProperty:"Normal",
            levelId:1,
            newCardInfo:[],
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
});