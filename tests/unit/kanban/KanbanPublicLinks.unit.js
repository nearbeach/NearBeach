// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanPublicLinks from "/src/js/components/kanban/KanbanPublicLinks.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('KanbanPublicLinks.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanPublicLinks, {
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