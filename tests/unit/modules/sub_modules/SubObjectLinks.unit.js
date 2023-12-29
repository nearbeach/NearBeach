// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import SubObjectLinks from "/src/js/components/modules/sub_modules/SubObjectLinks.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' SubObjectLinks.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(SubObjectLinks, {
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