// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import UpdateChangeLead from "/src/js/components/modules/wizards/UpdateChangeLead.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('UpdateChangeLead.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(UpdateChangeLead, {
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
