// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import AssociatedObjects from "/src/js/components/modules/sub_modules/AssociatedObjects.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' AssociatedObjects.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(AssociatedObjects, {
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