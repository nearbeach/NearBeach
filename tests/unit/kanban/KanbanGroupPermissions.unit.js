// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanGroupPermissions from "/src/js/components/kanban/KanbanGroupPermissions.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('KanbanGroupPermission.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanGroupPermissions, {
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