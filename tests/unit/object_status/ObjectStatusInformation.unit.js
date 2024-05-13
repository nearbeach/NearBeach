// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ParentModules from "/src/js/components/object_status/ObjectStatusInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ObjectStatusInformation.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ParentModules, {
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