// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanPropertyOrder from "/src/js/components/kanban/KanbanPropertyOrder.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('KanbanPropertyOrder.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanPropertyOrder, {
        props: {
            isDirty:false,
            isNewMode:false,
            kanbanBoardId:1,
            propertyList:[{"id":1,"property":"Normal","title":"Backlog"},{"id":2,"property":"Blocked","title":"Blocked"},{"id":3,"property":"Normal","title":"In Progress"},{"id":4,"property":"Normal","title":"Review and QA"},{"id":5,"property":"Closed","title":"Completed"}],
            propertyName:"Column",
            source:"columnModel",
        },
        global: {
            plugins: [store],
            mocks: {
                axios,
            }
        },
    });

    test('Empty test', () => {});
});