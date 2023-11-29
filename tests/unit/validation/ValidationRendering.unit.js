// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ValidationRendering from "/src/js/components/validation/ValidationRendering.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ValidationRendering, {
        props: {
            groupResults: [{"model":"NearBeach.group","pk":1,"fields":{"group_name":"Administration","parent_group":null,"date_created":"2023-02-15T08:56:14.216Z","date_modified":"2023-02-15T08:56:14.216Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":2,"fields":{"group_name":"QA Team","parent_group":null,"date_created":"2023-02-15T08:57:34.987Z","date_modified":"2023-02-15T08:57:34.987Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":3,"fields":{"group_name":"Empty Group","parent_group":null,"date_created":"2023-02-15T08:57:47.633Z","date_modified":"2023-02-15T08:57:47.633Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":4,"fields":{"group_name":"No Group","parent_group":null,"date_created":"2023-02-15T08:57:55.934Z","date_modified":"2023-02-15T08:57:55.934Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":5,"fields":{"group_name":"A simple group","parent_group":null,"date_created":"2023-11-22T08:37:21.246Z","date_modified":"2023-11-22T08:37:21.246Z","change_user":1,"is_deleted":false}}],
            rootUrl:"/",
            staticUrl:"/static/",
            statusList: [{"model":"NearBeach.listofrequirementstatus","pk":1,"fields":{"requirement_status":"Backlog","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":2,"fields":{"requirement_status":"Blocked","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":3,"fields":{"requirement_status":"In Progress","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":4,"fields":{"requirement_status":"Testing/Review","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}}],
            theme:"dark",
            typeList: [{"model":"NearBeach.listofrequirementtype","pk":1,"fields":{"requirement_type":"Non Specific","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementtype","pk":2,"fields":{"requirement_type":"Customer Requirements","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementtype","pk":3,"fields":{"requirement_type":"System Requirements","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}}],
            userGroupResults: [{"group_id":1,"group__group_name":"Administration"}],
            uuid:"289c3677-b28a-4018-847f-a8806e8b24d4",

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
