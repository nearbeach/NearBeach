// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import DashboardMyObjects from "/src/js/components/dashboard/DashboardMyObjects.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(DashboardMyObjects, {
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
