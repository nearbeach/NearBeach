// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ListTagsModule from "/src/js/components/modules/sub_modules/ListTagsModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ListTagsModule.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ListTagsModule, {
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