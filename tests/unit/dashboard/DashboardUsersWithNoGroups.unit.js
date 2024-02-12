// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import DashboardUsersWithNoGroups from "/src/js/components/dashboard/DashboardUsersWithNoGroups.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(DashboardUsersWithNoGroups, {
        props: {
        },
        global: {
            plugins: [store],
            properties: [axios],
            axios: axios,
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
});
