// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import AssignedSprints from "/src/js/components/modules/sub_modules/AssignedSprints.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' AssignedSprints.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(AssignedSprints, {
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