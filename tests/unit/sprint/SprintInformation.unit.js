// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ParentModules from "/src/js/components/sprints/SprintInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' SprintInformation.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ParentModules, {
        props: {
            rootUrl: "/",
            sprintResults: [{"sprint_id":2,"completed_story_points":0,"project":2,"requirement":null,"sprint_name":"project-2 - Sprint 1 - 18 Mar 2024","sprint_end_date":"2024-03-25T08:45:29.300Z","sprint_start_date":"2024-03-18T08:45:29.300Z","sprint_status":"Draft","total_story_points":0}],
            theme: "light",
            userLevel: 4,
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