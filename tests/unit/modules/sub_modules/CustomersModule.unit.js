// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CustomersModule from "/src/js/components/modules/sub_modules/CustomersModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' CustomersModule.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CustomersModule, {
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