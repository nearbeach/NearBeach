// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import NewKanbanCard from "/src/js/components/modules/wizards/NewKanbanCard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require("axios");

describe('NewKanbanCard.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(NewKanbanCard, {
        props: {
            columnResults:[{"model":"NearBeach.kanbancolumn","pk":31,"fields":{"kanban_column_name":"Backlog","kanban_column_property":"Normal","kanban_column_sort_number":0,"kanban_board":7,"date_created":"2023-11-06T09:29:54.639Z","date_modified":"2023-11-06T09:29:54.639Z","change_user":2,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":32,"fields":{"kanban_column_name":"Blocked","kanban_column_property":"Blocked","kanban_column_sort_number":1,"kanban_board":7,"date_created":"2023-11-06T09:29:54.640Z","date_modified":"2023-11-06T09:29:54.640Z","change_user":2,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":33,"fields":{"kanban_column_name":"In Progress","kanban_column_property":"Normal","kanban_column_sort_number":2,"kanban_board":7,"date_created":"2023-11-06T09:29:54.642Z","date_modified":"2023-11-06T09:29:54.642Z","change_user":2,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":34,"fields":{"kanban_column_name":"Review and QA","kanban_column_property":"Normal","kanban_column_sort_number":3,"kanban_board":7,"date_created":"2023-11-06T09:29:54.644Z","date_modified":"2023-11-06T09:29:54.644Z","change_user":2,"is_deleted":false}},{"model":"NearBeach.kanbancolumn","pk":35,"fields":{"kanban_column_name":"Completed","kanban_column_property":"Closed","kanban_column_sort_number":4,"kanban_board":7,"date_created":"2023-11-06T09:29:54.646Z","date_modified":"2023-11-06T09:29:54.646Z","change_user":2,"is_deleted":false}}],
            kanbanBoardResults:[{"model":"NearBeach.kanbanboard","pk":7,"fields":{"kanban_board_name":"Opened KAB","requirement":null,"kanban_board_status":"Open","date_created":"2023-11-06T09:29:54.636Z","date_modified":"2023-11-06T09:29:54.636Z","change_user":2,"creation_user":2,"is_deleted":false}}],
            kanbanCardResults:[{"model":"NearBeach.kanbancard","pk":24,"fields":{"kanban_card_text":"asdf","kanban_card_description":"undefined","kanban_card_sort_number":0,"kanban_level":19,"kanban_column":31,"kanban_board":7,"kanban_card_priority":0,"project":null,"task":null,"requirement":null,"is_archived":false,"date_created":"2023-11-06T09:29:58.470Z","date_modified":"2023-11-08T10:24:14.130Z","change_user":2,"is_deleted":false}}],
            levelResults:[{"model":"NearBeach.kanbanlevel","pk":18,"fields":{"kanban_level_name":"Sprint 1","kanban_level_sort_number":0,"kanban_board":7,"date_created":"2023-11-06T09:29:54.648Z","date_modified":"2023-11-06T09:29:54.648Z","change_user":2,"is_deleted":false}},{"model":"NearBeach.kanbanlevel","pk":19,"fields":{"kanban_level_name":"Sprint 2","kanban_level_sort_number":1,"kanban_board":7,"date_created":"2023-11-06T09:29:54.650Z","date_modified":"2023-11-06T09:29:54.650Z","change_user":2,"is_deleted":false}}],
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
