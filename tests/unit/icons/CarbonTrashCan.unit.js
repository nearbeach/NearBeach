// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CarbonTrashCan from "/src/js/components/icons/CarbonTrashCan.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CarbonTrashCan, {
        props: {
        },
    });

    test('Empty test', () => {});
});
