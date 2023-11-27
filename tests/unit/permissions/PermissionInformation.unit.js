// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import PermissionInformation from "/src/js/components/permissions/PermissionInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(PermissionInformation, {
        props: {
            permissionBoolean: [[0,"No Permission"],[1,"Has Permission"]],
            permissionLevel: [[0,"No Permission"],[1,"Read Only"],[2,"Edit Only"],[3,"Add and Edit"],[4,"Full Permission"]],
            permissionSetResults: [{"model":"NearBeach.permissionset","pk":3,"fields":{"permission_set_name":"Add and Edit","administration_assign_user_to_group":0,"administration_create_group":0,"administration_create_permission_set":0,"administration_create_user":0,"bug_client":3,"customer":3,"kanban_board":3,"kanban_card":3,"organisation":3,"project":3,"request_for_change":3,"requirement":3,"task":3,"tag":3,"document":0,"kanban_comment":0,"project_history":0,"task_history":0,"date_created":"2023-02-15T09:00:25.979Z","date_modified":"2023-05-24T11:23:06.295Z","change_user":1,"is_deleted":false}}],
            rootUrl:"/",
            theme:"dark",
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
