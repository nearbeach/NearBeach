// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ConfirmPermissionDelete from "/src/js/components/administration/ConfirmPermissionDelete.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('ConfirmPermissionDelete.vue', () => {
    //Using mount - insert data
    const wrapper = mount(ConfirmPermissionDelete, {
        props: {
            permissionDeleteId: 0,
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
