// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RequirementInformation from "/src/js/components/requirements/RequirementInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RequirementInformation, {
        props: {
            defaultStakeholderImage:"/static/NearBeach/images/placeholder/product_tour.svg",
            organisationResults:[{"model":"NearBeach.organisation","pk":1,"fields":{"organisation_name":"NearBeach Incorporate","organisation_website":"https://nearbeach.org","organisation_email":"support@nearbeach.org","organisation_profile_picture":null,"date_created":"2023-02-15T08:56:40.669Z","date_modified":"2023-02-15T08:56:40.669Z","change_user":1,"is_deleted":false}}],
            requirementResults:[{"model":"NearBeach.requirement","pk":1,"fields":{"requirement_title":"Requirement - Administration","requirement_scope":"<p>Requirement - Administration</p>","requirement_type":2,"requirement_status":3,"requirement_story_point_min":1,"requirement_story_point_max":4,"organisation":1,"date_created":"2023-02-15T09:17:21.805Z","date_modified":"2023-02-15T09:17:21.805Z","change_user":1,"creation_user":1,"is_deleted":false}}],
            statusList:[{"model":"NearBeach.listofrequirementstatus","pk":1,"fields":{"requirement_status":"Backlog","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":2,"fields":{"requirement_status":"Blocked","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":3,"fields":{"requirement_status":"In Progress","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":4,"fields":{"requirement_status":"Testing/Review","requirement_status_is_closed":false,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementstatus","pk":5,"fields":{"requirement_status":"Closed","requirement_status_is_closed":true,"date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}}],
            theme:"dark",
            typeList:[{"model":"NearBeach.listofrequirementtype","pk":1,"fields":{"requirement_type":"Non Specific","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementtype","pk":2,"fields":{"requirement_type":"Customer Requirements","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementtype","pk":3,"fields":{"requirement_type":"System Requirements","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}}],
            userLevel:4,
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
