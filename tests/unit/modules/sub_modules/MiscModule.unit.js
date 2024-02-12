// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import MiscModule from "/src/js/components/modules/sub_modules/MiscModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' MiscModule.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(MiscModule, {
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