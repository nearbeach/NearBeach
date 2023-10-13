// Vitest
import { describe, expect, test } from "vitest";
import {mount, VueWrapper} from "@vue/test-utils";

// Import vue component
import ChangeTaskInformation from "/src/js/components/change_task/ChangeTaskInformation.vue";

// VueX
import { store } from "/src/js/vuex-store";

describe('AdminAddUser.vue - rendering component', () => {
    //Using mount - insert data
    const wrapper = mount(ChangeTaskInformation, {
        props: {
            changeTaskResults: [
                {
                    "model":"NearBeach.changetask",
                    "pk":1,
                    "fields":{
                        "request_for_change":1,
                        "change_task_title":"Administration - Back up - Change Task",
                        "change_task_description":"<p>Description is optional</p>",
                        "change_task_start_date":"2023-02-14T22:00:00Z",
                        "change_task_end_date":"2023-03-01T05:00:00Z",
                        "change_task_seconds":1234800000,
                        "change_task_assigned_user":1,
                        "change_task_qa_user":2,
                        "change_task_required_by":"Stakeholder(s)",
                        "change_task_status":1,
                        "is_downtime":false,
                        "date_created":"2023-02-15T09:15:34.805Z",
                        "date_modified":"2023-10-06T10:05:33.935Z",
                        "change_user":1,
                        "creation_user":1,
                        "is_deleted":false
                    }
                },
            ],
            destination: "change_task",
            locationId: 1,
            rfcStatus: "Draft",
            userLevel: 4,
            userList: [
                {
                    "id":1,
                    "email":"support@nearbeach.org",
                    "first_name": "Admin",
                    "last_name":"User",
                    "username":"admin"
                },
                {
                    "id":2,
                    "email":"support@nearbeach.org",
                    "first_name":"Team",
                    "last_name":"Leader",
                    "username":"team_leader"
                },
                {
                    "id":3,
                    "email":"support@nearbeach.org",
                    "first_name":"Team",
                    "last_name":"Member",
                    "username":"team_member"
                },
                {
                    "id":4,
                    "email":"support@nearbeach.org",
                    "first_name":"Team",
                    "last_name":"Intern",
                    "username":"team_intern"
                },
                {
                    "id":5,
                    "email":"support@nearbeach.org",
                    "first_name":"Read",
                    "last_name":"Only",
                    "username":"read_only"
                },
                {
                    "id":6,
                    "email":"support@nearbeach.org",
                    "first_name":"No",
                    "last_name":"Group",
                    "username":"no_group"
                },
                {
                    "id":7,
                    "email":"support@nearbeach.org",
                    "first_name":"Dark",
                    "last_name":"Admin",
                    "username":"dark_admin"
                }
            ],
        },
        global: {
            plugins: [store],
        },
    });

    test('Empty test', () => {});
});
