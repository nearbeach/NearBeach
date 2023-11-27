// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RenderToasts from "/src/js/components/render/RenderToasts.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RenderToasts, {
        props: {},
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {
    });
})
