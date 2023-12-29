// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import GroupsAndUsersModule from "/src/js/components/modules/sub_modules/GroupsAndUsersModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' GroupsAndUsersModule.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(GroupsAndUsersModule, {
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