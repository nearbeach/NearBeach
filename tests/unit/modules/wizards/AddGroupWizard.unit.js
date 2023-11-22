// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import AddGroupWizard from "/src/js/components/modules/wizards/AddGroupWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('AddGroupWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(AddGroupWizard, {
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
