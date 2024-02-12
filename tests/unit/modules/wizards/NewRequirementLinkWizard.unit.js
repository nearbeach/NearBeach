// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NewRequirementLinkWizard from "/src/js/components/modules/wizards/NewRequirementLinkWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewRequirementLinkWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NewRequirementLinkWizard, {
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
