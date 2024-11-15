// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ConfirmChangeTaskDelete from "/src/js/components/change_task/modules/ConfirmChangeTaskDelete.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ConfirmChangeTaskDelete, {
        props: {
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
