// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CarbonDocumentPdf from "/src/js/components/icons/CarbonDocumentPdf.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CarbonDocumentPdf, {
        props: {
        },
    });

    test('Empty test', () => {});
});
