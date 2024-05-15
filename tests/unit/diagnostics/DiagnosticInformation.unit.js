// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import BetweenDates from "/src/js/components/diagnostic/DiagnosticInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('DiagnosticInformation.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(BetweenDates, {
        props: {
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
