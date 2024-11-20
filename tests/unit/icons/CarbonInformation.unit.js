// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CarbonInformation from "/src/js/components/icons/CarbonInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CarbonInformation, {
        props: {
        },
    });

    test('Empty test', () => {});
});
