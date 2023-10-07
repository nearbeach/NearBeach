// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CardNotes from "/src/js/components/card_information/CardNotes.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CardNotes, {
        props: {
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
