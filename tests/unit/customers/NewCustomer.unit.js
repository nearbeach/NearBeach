// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NewCustomer from "/src/js/components/customers/NewCustomer.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NewCustomer, {
        props: {
            titleList: [{"model":"NearBeach.listoftitle","pk":1,"fields":{"title":"Mr","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listoftitle","pk":2,"fields":{"title":"Ms","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listoftitle","pk":3,"fields":{"title":"Mrs","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listoftitle","pk":4,"fields":{"title":"Mx","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}}],
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