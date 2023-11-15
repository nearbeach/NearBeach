// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import AddCustomerWizard from "/src/js/components/modules/wizards/AddCustomerWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('AddCustomerWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(AddCustomerWizard, {
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
