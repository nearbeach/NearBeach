// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ChildSprints from "/src/js/components/modules/sub_modules/ChildSprints.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ChildSprints.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ChildSprints, {
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