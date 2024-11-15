// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RenderUserCardList from "/src/js/components/render/RenderUserCardList.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RenderUserCardList, {
        props: {},
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {
    });
})
