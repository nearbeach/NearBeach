// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CarbonConnectionFlowUsage from "/src/js/components/icons/CarbonConnectionFlowUsage.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('CarbonConnectionFlowUsage.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CarbonConnectionFlowUsage, {
        props: {
        },
    });

    test('Empty test', () => {});
});
