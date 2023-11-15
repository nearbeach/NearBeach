// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ListNotes from "/src/js/components/modules/sub_modules/ListNotes.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ListNotes.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ListNotes, {
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