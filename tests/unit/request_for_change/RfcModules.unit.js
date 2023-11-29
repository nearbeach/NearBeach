// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import RfcModules from "/src/js/components/request_for_change/RfcModules.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(RfcModules, {
        props: {
            destination: "request_for_change",
            isReadOnly: true,
            locationId: 1,
            rfcResults: [{"model":"NearBeach.requestforchange","pk":1,"fields":{"rfc_title":"RFC - Admin","rfc_summary":"<p>Request for Change - admin</p>","rfc_type":2,"rfc_implementation_start_date":"2023-02-14T22:00:00Z","rfc_implementation_end_date":"2023-03-01T05:00:00Z","rfc_implementation_release_date":"2023-03-01T06:00:00Z","rfc_version_number":"0.30.0","rfc_status":2,"rfc_lead":1,"rfc_priority":2,"rfc_risk":3,"rfc_impact":2,"rfc_risk_and_impact_analysis":"<p>Risk Association</p>","rfc_implementation_plan":"<p>Implementation Plan</p>","rfc_backout_plan":"<p>Backout plan</p>","rfc_test_plan":"<p>Test Plan</p>","date_created":"2023-02-15T09:15:05.013Z","date_modified":"2023-11-27T09:34:01.355Z","change_user":1,"creation_user":1,"is_deleted":false}}],
            theme: "",
            userList: [{"id":1,"email":"support@nearbeach.org","first_name":"Admin","last_name":"User","username":"admin"},{"id":7,"email":"support@nearbeach.org","first_name":"Dark","last_name":"Admin","username":"dark_admin"}],
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
