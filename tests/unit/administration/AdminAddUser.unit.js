// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import AdminAddUser from "/src/js/components/administration/AdminAddUser.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(AdminAddUser, {
        props: {
            destination: "project",
            locationId: 1,
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});