// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import UserInformation from "/src/js/components/users/UserInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(UserInformation, {
        props: {
            rootUrl:"/",
            userResults:[{"model":"auth.user","pk":7,"fields":{"password":"pbkdf2_sha256$600000$mm3IyCbjcofqWTSssaWcu6$dmbngBObwSr8Glv4jKyL1LandqtPNJ3epNfTT9dTs4U=","last_login":"2023-11-22T10:57:06.155Z","is_superuser":true,"username":"dark_admin","first_name":"Dark","last_name":"Admin","email":"support@nearbeach.org","is_staff":false,"is_active":true,"date_joined":"2023-09-06T09:36:15.453Z","groups":[],"user_permissions":[]}}],
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
