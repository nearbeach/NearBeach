// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import CustomerInformation from "/src/js/components/customers/CustomerInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('NewChangeTask.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(CustomerInformation, {
        props: {
            customerResults: [
                {
                    "model":"NearBeach.customer",
                    "pk":1,
                    "fields": {
                        "customer_title":2,
                        "customer_first_name":"Socks",
                        "customer_last_name":"Fluffy",
                        "customer_email":"socks@nearbeach.org",
                        "customer_profile_picture":null,
                        "organisation":1,
                        "date_created":"2023-02-15T08:57:03.560Z",
                        "date_modified":"2023-02-15T08:57:03.560Z",
                        "change_user":1,
                        "is_deleted":false
                    }
                }
            ],
            organisationResults: [{"model":"NearBeach.organisation","pk":1,"fields":{"organisation_name":"NearBeach Incorporate","organisation_website":"https://nearbeach.org","organisation_email":"support@nearbeach.org","organisation_profile_picture":null,"date_created":"2023-02-15T08:56:40.669Z","date_modified":"2023-02-15T08:56:40.669Z","change_user":1,"is_deleted":false}}],
            titleList: [{"model":"NearBeach.listoftitle","pk":1,"fields":{"title":"Mr","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listoftitle","pk":2,"fields":{"title":"Ms","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listoftitle","pk":3,"fields":{"title":"Mrs","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}},{"model":"NearBeach.listoftitle","pk":4,"fields":{"title":"Mx","date_created":"2023-02-15T08:51:58.374Z","date_modified":"2023-02-15T08:51:58.374Z","change_user":null,"is_deleted":false}}],
            userLevel: 4,
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
