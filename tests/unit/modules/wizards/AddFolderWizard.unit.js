// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import AddFolderWizard from "/src/js/components/modules/wizards/AddFolderWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('AddFolderWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(AddFolderWizard, {
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
