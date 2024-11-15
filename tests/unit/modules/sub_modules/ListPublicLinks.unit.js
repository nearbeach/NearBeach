// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ListPublicLinks from "/src/js/components/modules/sub_modules/ListPublicLinks.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ListPublicLinks.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ListPublicLinks, {
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