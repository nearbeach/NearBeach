// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import DashboardKanbanList from "/src/js/components/dashboard/DashboardKanbanList.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(DashboardKanbanList, {
        props: {
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            },
        },
    });

    test('Empty test', () => {});
});
