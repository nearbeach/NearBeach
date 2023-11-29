// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RequirementItemInformation from "/src/js/components/requirement_items/RequirementItemInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RequirementItemInformation, {
        props: {
            defaultStakeholderImage:"/static/NearBeach/images/placeholder/product_tour.svg",
            organisationResults: [{"model":"NearBeach.organisation","pk":1,"fields":{"organisation_name":"NearBeach Incorporate","organisation_website":"https://nearbeach.org","organisation_email":"support@nearbeach.org","organisation_profile_picture":null,"date_created":"2023-02-15T08:56:40.669Z","date_modified":"2023-02-15T08:56:40.669Z","change_user":1,"is_deleted":false}}],
            requirementItemResults: [{"model":"NearBeach.requirementitem","pk":1,"fields":{"requirement":1,"requirement_item_title":"Requirement Item - Administration Only","requirement_item_scope":"<p>Requirement Item - Administration Only</p>","requirement_item_status":3,"requirement_item_type":4,"ri_story_point_min":4,"ri_story_point_max":10,"date_created":"2023-02-15T09:17:45.806Z","date_modified":"2023-02-15T09:17:45.806Z","change_user":1,"is_deleted":false}}],
            statusList: [{"model":"NearBeach.listofrequirementitemstatus","pk":1,"fields":{"requirement_item_status":"Draft","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":2,"fields":{"requirement_item_status":"Review","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":3,"fields":{"requirement_item_status":"Developing/Working","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":4,"fields":{"requirement_item_status":"Testing","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":5,"fields":{"requirement_item_status":"User Acceptance Testing","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":6,"fields":{"requirement_item_status":"Rework","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":7,"fields":{"requirement_item_status":"Implemented","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":8,"fields":{"requirement_item_status":"Finish","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":9,"fields":{"requirement_item_status":"Not Tested","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemstatus","pk":10,"fields":{"requirement_item_status":"Obsolete","status_is_closed":false,"date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}}],
            theme:"dark",
            typeList: [{"model":"NearBeach.listofrequirementitemtype","pk":1,"fields":{"requirement_item_type":"Informational","date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemtype","pk":2,"fields":{"requirement_item_type":"Feature","date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemtype","pk":3,"fields":{"requirement_item_type":"User Case","date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemtype","pk":4,"fields":{"requirement_item_type":"User Interface","date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemtype","pk":5,"fields":{"requirement_item_type":"Non Functional","date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.372Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemtype","pk":6,"fields":{"requirement_item_type":"Constraint","date_created":"2023-02-15T08:51:58.372Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listofrequirementitemtype","pk":7,"fields":{"requirement_item_type":"System Function","date_created":"2023-02-15T08:51:58.373Z","date_modified":"2023-02-15T08:51:58.373Z","change_user":null,"is_deleted":false}}],
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
