// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import TaskInformation from "/src/js/components/tasks/TaskInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(TaskInformation, {
        props: {
            defaultStakeholderImage:"/static/NearBeach/images/placeholder/product_tour.svg",
            groupResults:[],
            organisationResults:[{"model":"NearBeach.organisation","pk":1,"fields":{"organisation_name":"NearBeach Incorporate","organisation_website":"https://nearbeach.org","organisation_email":"support@nearbeach.org","organisation_profile_picture":null,"date_created":"2023-02-15T08:56:40.669Z","date_modified":"2023-02-15T08:56:40.669Z","change_user":1,"is_deleted":false}}],
            stakeholderModel:[],
            taskResults:[{"model":"NearBeach.task","pk":1,"fields":{"task_short_description":"Task - Administration","task_long_description":"<p>Task - Administration</p>","organisation":1,"task_start_date":"2023-02-14T22:00:00Z","task_end_date":"2023-03-01T05:00:00Z","task_assigned_to":null,"task_status":"New","task_story_point_min":4,"task_story_point_max":10,"date_created":"2023-02-15T09:19:37.972Z","date_modified":"2023-02-15T09:19:37.972Z","change_user":1,"creation_user":1,"is_deleted":false}}],
            theme:"dark",
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
