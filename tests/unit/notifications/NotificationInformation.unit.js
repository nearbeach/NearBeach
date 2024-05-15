// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ParentModules from "/src/js/components/notifications/NotificationInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' NotificationInformation.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ParentModules, {
        props: {
            notificationResults: [{"model":"NearBeach.notification","pk":1,"fields":{"notification_header":"A simple notification for everyone","notification_message":"Please ignore - this is a fixture notification","notification_start_date":"2023-11-14T22:00:00Z","notification_end_date":"2099-11-27T05:00:00Z","notification_location":"all","date_created":"2023-11-15T11:05:26.869Z","date_modified":"2023-11-15T11:05:26.869Z","change_user":null,"is_deleted":false}}],
            rootUrl: "/",
            staticUrl: "/static/",
            theme: "light",
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
})