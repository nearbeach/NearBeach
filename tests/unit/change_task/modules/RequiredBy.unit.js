// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RequiredBy from "/src/js/components/change_task/modules/RequiredBy.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RequiredBy, {
        props: {
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
