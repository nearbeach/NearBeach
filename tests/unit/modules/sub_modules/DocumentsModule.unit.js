// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import DocumentsModule from "/src/js/components/modules/sub_modules/DocumentsModule.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('ChangeTaskModules.vue - rendering component.', () => {
    //Using mount - insert data
    const wrapper = mount(DocumentsModule, {
        props: {
            overrideDestination:"",
            overrideLocationId:0,
            readOnly:false,
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
});

