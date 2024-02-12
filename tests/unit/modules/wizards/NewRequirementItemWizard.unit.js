// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NewRequirementItemWizard from "/src/js/components/modules/wizards/NewRequirementItemWizard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewRequirementItemWizard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NewRequirementItemWizard, {
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
