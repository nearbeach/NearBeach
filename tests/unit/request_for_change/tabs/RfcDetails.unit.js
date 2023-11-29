// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RfcDetails from "/src/js/components/request_for_change/tabs/RfcDetails.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RfcDetails, {
        props: {
            groupResults: [{"model":"NearBeach.group","pk":1,"fields":{"group_name":"Administration","parent_group":null,"date_created":"2023-02-15T08:56:14.216Z","date_modified":"2023-02-15T08:56:14.216Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":2,"fields":{"group_name":"QA Team","parent_group":null,"date_created":"2023-02-15T08:57:34.987Z","date_modified":"2023-02-15T08:57:34.987Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":3,"fields":{"group_name":"Empty Group","parent_group":null,"date_created":"2023-02-15T08:57:47.633Z","date_modified":"2023-02-15T08:57:47.633Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":4,"fields":{"group_name":"No Group","parent_group":null,"date_created":"2023-02-15T08:57:55.934Z","date_modified":"2023-02-15T08:57:55.934Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":5,"fields":{"group_name":"A simple group","parent_group":null,"date_created":"2023-11-22T08:37:21.246Z","date_modified":"2023-11-22T08:37:21.246Z","change_user":1,"is_deleted":false}}],
            userGroupResults: [{"group_id":1,"group__group_name":"Administration"}],
            uuid:"b9001bee-3486-4597-983f-7addcc2469dc",
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {
    });
})
