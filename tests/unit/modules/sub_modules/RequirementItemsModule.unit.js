// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RequirementItemsModule from "/src/js/components/modules/sub_modules/RequirementItemsModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('RequirementItemsModule.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RequirementItemsModule, {
        props: {
            destination: "project",
            locationId: 1,
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
})