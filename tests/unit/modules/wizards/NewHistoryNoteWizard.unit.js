// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NewHistoryNoteWizard from "/src/js/components/modules/wizards/NewHistoryNoteWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewHistoryNoteWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NewHistoryNoteWizard, {
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
