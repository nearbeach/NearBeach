// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import UploadDocumentWizard from "/src/js/components/modules/wizards/UploadDocumentWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('UploadDocumentWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(UploadDocumentWizard, {
        props: {},
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
})
