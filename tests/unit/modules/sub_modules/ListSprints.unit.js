// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ListSprints from "/src/js/components/modules/sub_modules/ListSprints.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ListSprints.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ListSprints, {
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