// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ProfileInformation from "/src/js/components/profile/ProfileInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ProfileInformation, {
        props: {
            rootUrl: "/",
            staticUrl: "/static/",
            theme: "dark",
            userResults: [{"id":7,"username":"dark_admin","first_name":"Dark","last_name":"Admin","email":"support@nearbeach.org"}],
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
