// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NewKanban from "/src/js/components/kanban/NewKanban.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe(' NewKanban.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NewKanban, {
        props: {},
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
});