// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RequirementItemLinksModule from "/src/js/components/modules/sub_modules/RequirementItemLinksModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' RequirementItemLinksModule.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RequirementItemLinksModule, {
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