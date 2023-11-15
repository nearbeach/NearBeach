// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import UserList from "/src/js/components/administration/UserList.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(UserList, {
        props: {
            destination: "user",
            locationId: 1,
            theme: "light",
            userListResults: [
                {
                    "user_group_id":1,
                    "username":1,
                    "username__first_name":"Socks",
                    "username__last_name":"Fluffybutt",
                    "username__email":"support@nearbeach.org",
                    "group":1,
                    "group__group_name":"Administration",
                    "group_leader":true,
                    "permission_set":1,
                    "permission_set__permission_set_name":"Administration Permission Set"
                },
            ],
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