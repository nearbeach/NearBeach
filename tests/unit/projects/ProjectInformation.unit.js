// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ProjectInformation from "/src/js/components/projects/ProjectInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ProjectInformation, {
        props: {
            defaultStakeholderImage: "/static/NearBeach/images/placeholder/product_tour.svg",
            organisationResults: [{"model":"NearBeach.organisation","pk":1,"fields":{"organisation_name":"NearBeach Incorporate","organisation_website":"https://nearbeach.org","organisation_email":"support@nearbeach.org","organisation_profile_picture":null,"date_created":"2023-02-15T08:56:40.669Z","date_modified":"2023-02-15T08:56:40.669Z","change_user":1,"is_deleted":false}}],
            projectResults: [{"model":"NearBeach.project","pk":1,"fields":{"project_name":"Project - Only Administration","project_description":"<p>Project - Only Administration</p>","organisation":1,"customer":null,"project_start_date":"2023-02-14T22:00:00Z","project_end_date":"2023-03-01T05:00:00Z","project_status":"New","project_story_point_min":1,"project_story_point_max":4,"date_created":"2023-02-15T09:13:53.432Z","date_modified":"2023-02-15T09:13:53.432Z","change_user":1,"creation_user":1,"is_deleted":false}}],
            theme: "dark",
            userLevel: 4,
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
