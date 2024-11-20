// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ConfirmKanbanBoardReopen from "/src/js/components/kanban/ConfirmKanbanBoardReopen.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('ConfirmKanbanBoardReopen.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ConfirmKanbanBoardReopen, {
        props: {},
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
})