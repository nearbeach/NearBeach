// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ObjectLinks from "/src/js/components/modules/sub_modules/ObjectLinks.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ObjectLinks.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ObjectLinks, {
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