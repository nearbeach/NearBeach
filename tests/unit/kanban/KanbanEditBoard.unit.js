// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanEditBoard from "/src/js/components/kanban/KanbanEditBoard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('KanbanEditBoard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanEditBoard, {
        props: {
            columnResults:[{"model":"NearBeach.kanbancolumn","pk":1,"fields":{"kanban_column_name":"Backlog","kanban_column_property":"Normal","kanban_column_sort_number":0,"kanban_board":1,"date_created":"2023-02-15T09:12:31.597Z","date_modified":"2023-02-15T09:12:31.597Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":2,"fields":{"kanban_column_name":"Blocked","kanban_column_property":"Blocked","kanban_column_sort_number":1,"kanban_board":1,"date_created":"2023-02-15T09:12:31.599Z","date_modified":"2023-02-15T09:12:31.599Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":3,"fields":{"kanban_column_name":"In Progress","kanban_column_property":"Normal","kanban_column_sort_number":2,"kanban_board":1,"date_created":"2023-02-15T09:12:31.600Z","date_modified":"2023-02-15T09:12:31.600Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":4,"fields":{"kanban_column_name":"Review and QA","kanban_column_property":"Normal","kanban_column_sort_number":3,"kanban_board":1,"date_created":"2023-02-15T09:12:31.600Z","date_modified":"2023-02-15T09:12:31.601Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":5,"fields":{"kanban_column_name":"Completed","kanban_column_property":"Closed","kanban_column_sort_number":4,"kanban_board":1,"date_created":"2023-02-15T09:12:31.601Z","date_modified":"2023-02-15T09:12:31.602Z","change_user":1,"is_deleted":false}}],
            kanbanBoardResults:[{"model":"NearBeach.kanbanboard","pk":1,"fields":{"kanban_board_name":"Kanban Admin Only","requirement":null,"kanban_board_status":"Open","date_created":"2023-02-15T09:12:31.594Z","date_modified":"2023-02-15T09:12:31.594Z","change_user":1,"creation_user":1,"is_deleted":false}}],
            levelResults:[{"model":"NearBeach.kanbanlevel","pk":1,"fields":{"kanban_level_name":"Sprint 1","kanban_level_sort_number":0,"kanban_board":1,"date_created":"2023-02-15T09:12:31.603Z","date_modified":"2023-02-15T09:12:31.603Z","change_user":1,"is_deleted":false}},{"model":"NearBeach.kanbanlevel","pk":2,"fields":{"kanban_level_name":"Sprint 2","kanban_level_sort_number":1,"kanban_board":1,"date_created":"2023-02-15T09:12:31.604Z","date_modified":"2023-02-15T09:12:31.604Z","change_user":1,"is_deleted":false}}],
            locationId:1,
            rootUrl:"/",
            staticUrl:"/static/",
            theme:"dark",
            userLevel:4
        },
        global: {
            plugins: [store],
            mocks: {
                // axios,
            }
        },
    });

    test('Empty test', () => {});
});