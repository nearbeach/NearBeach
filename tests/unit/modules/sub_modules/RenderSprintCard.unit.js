// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RenderSprintCard from "/src/js/components/modules/sub_modules/RenderSprintCard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' RenderSprintCard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RenderSprintCard, {
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