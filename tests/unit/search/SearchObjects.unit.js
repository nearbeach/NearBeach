// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import SearchObjects from "/src/js/components/search/SearchObjects.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe(' ParentModules.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(SearchObjects, {
        props: {
            includeClosed:false,
            rootUrl:"/",
            searchInput:"",
            searchResults:{"request_for_change":[{"rfc_id":1,"rfc_title":"RFC - Admin","rfc_status":2,"rfc_status__rfc_status":"Waiting for approval"},{"rfc_id":2,"rfc_title":"RFC - QA Team","rfc_status":1,"rfc_status__rfc_status":"Draft"}],"requirement":[{"requirement_id":1,"requirement_title":"Requirement - Administration","requirement_status__requirement_status":"In Progress"},{"requirement_id":2,"requirement_title":"Requirement - QA Team","requirement_status__requirement_status":"In Progress"}],"project":[{"project_id":1,"project_name":"Project - Only Administration","project_status":"New"},{"project_id":2,"project_name":"Project - QA Team","project_status":"New"}],"task":[{"task_id":1,"task_short_description":"Task - Administration","task_status":"New"},{"task_id":2,"task_short_description":"Task - QA Team","task_status":"New"}],"kanban":[{"kanban_board_id":1,"kanban_board_name":"Kanban Admin Only","kanban_board_status":"Open"},{"kanban_board_id":2,"kanban_board_name":"Kanban QA Team","kanban_board_status":"Open"}]},
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
