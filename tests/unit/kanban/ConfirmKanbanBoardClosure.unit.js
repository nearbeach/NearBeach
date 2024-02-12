// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ConfirmKanbanBoardClosure from "/src/js/components/kanban/ConfirmKanbanBoardClosure.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('ConfirmKanbanBoardClosure.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ConfirmKanbanBoardClosure, {
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