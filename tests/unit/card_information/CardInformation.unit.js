// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CardInformation from "/src/js/components/card_information/CardInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CardInformation, {
        props: {
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
        inject: ["nextTick"],
    });

    test('Empty test', () => {});
});
