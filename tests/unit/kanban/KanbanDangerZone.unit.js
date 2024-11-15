// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanDangerZone from "/src/js/components/kanban/KanbanDangerZone.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('KanbanDangerZone.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanDangerZone, {
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