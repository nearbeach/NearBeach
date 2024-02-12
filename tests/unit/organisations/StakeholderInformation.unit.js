// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import StakeholderInformation from "/src/js/components/organisations/StakeholderInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(StakeholderInformation, {
        props: {
            organisationResults:[{"model":"NearBeach.organisation","pk":1,"fields":{"organisation_name":"NearBeach Incorporate","organisation_website":"https://nearbeach.org","organisation_email":"support@nearbeach.org","organisation_profile_picture":null,"date_created":"2023-02-15T08:56:40.669Z","date_modified":"2023-02-15T08:56:40.669Z","change_user":1,"is_deleted":false}}],
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
