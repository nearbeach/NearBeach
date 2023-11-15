// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import KanbanBoard from "/src/js/components/kanban/KanbanBoard.vue";

// VueX
import { store } from "/src/js/vuex-store";

// Axios
const axios = require('axios');

describe('BlockedNotesModal.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(KanbanBoard, {
        props: {
            kanbanBoardResults: [{"model":"NearBeach.kanbanboard","pk":1,"fields":{"kanban_board_name":"Kanban Admin Only","requirement":null,"kanban_board_status":"Open","date_created":"2023-02-15T09:12:31.594Z","date_modified":"2023-02-15T09:12:31.594Z","change_user":1,"creation_user":1,"is_deleted":false}}],
            newCardInfo: [],
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