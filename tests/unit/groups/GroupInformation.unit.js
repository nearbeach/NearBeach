// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import GroupInformation from "/src/js/components/groups/GroupInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(GroupInformation, {
        props: {
            groupResults: [{"model":"NearBeach.group","pk":2,"fields":{"group_name":"QA Team","parent_group":null,"date_created":"2023-02-15T08:57:34.987Z","date_modified":"2023-02-15T08:57:34.987Z","change_user":1,"is_deleted":false}}],
            parentGroupResults: [{"model":"NearBeach.group","pk":1,"fields":{"group_name":"Administration","parent_group":null,"date_created":"2023-02-15T08:56:14.216Z","date_modified":"2023-02-15T08:56:14.216Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":2,"fields":{"group_name":"QA Team","parent_group":null,"date_created":"2023-02-15T08:57:34.987Z","date_modified":"2023-02-15T08:57:34.987Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":3,"fields":{"group_name":"Empty Group","parent_group":null,"date_created":"2023-02-15T08:57:47.633Z","date_modified":"2023-02-15T08:57:47.633Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.group","pk":4,"fields":{"group_name":"No Group","parent_group":null,"date_created":"2023-02-15T08:57:55.934Z","date_modified":"2023-02-15T08:57:55.934Z","change_user":1,"is_deleted":false}}],
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
