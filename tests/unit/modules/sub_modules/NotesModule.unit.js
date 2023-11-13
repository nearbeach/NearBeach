// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NotesModule from "/src/js/components/modules/sub_modules/NotesModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' NotesModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NotesModule, {
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