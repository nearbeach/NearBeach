// permission.spec.ts
import {setActivePinia, createPinia} from "pinia";
import {describe, test, expect, beforeEach} from "vitest";
import {usePermissionStore} from "@/stores/permissions/permission.ts";

describe("Permission store - _getMaximumFieldValue action", async () => {
    beforeEach(() => {
        setActivePinia(createPinia());
    });

    test("Permission Data is empty, and thus everything returns a 0", async () => {
        const permissionStore = usePermissionStore();

        expect(permissionStore._getMaximumFieldValue("administration_assign_user_to_group")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("administration_create_group")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("administration_create_permission_set")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("administration_create_user")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("customer")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("document")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("group_name")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("kanban_board")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("organisation")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("organisation_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("project")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("project_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("request_for_change")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement_item_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("schedule_object")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("sprint")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("task")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("tag")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("kanban_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("task_note")).toBe(0);
    });

     test("Test with fake field", async () => {
        const permissionStore = usePermissionStore();

        // Set the data
        permissionStore.permissionData = [
            {
                "administration_assign_user_to_group": 4,
                "administration_create_group": 4,
                "administration_create_permission_set": 4,
                "administration_create_user": 4,
                "customer": 4,
                "document": 1,
                "group_id": 1,
                "group_name": "Administration",
                "kanban_board": 4,
                "organisation": 4,
                "organisation_note": 1,
                "project": 4,
                "project_note": 1,
                "request_for_change": 4,
                "requirement": 4,
                "requirement_item_note": 1,
                "requirement_note": 1,
                "schedule_object": 4,
                "sprint": 1,
                "task": 4,
                "tag": 4,
                "kanban_note": 1,
                "task_note": 1
            },
            {
                "administration_assign_user_to_group": 0,
                "administration_create_group": 0,
                "administration_create_permission_set": 0,
                "administration_create_user": 0,
                "customer": 0,
                "document": 0,
                "group_id": 0,
                "group_name": "QA Team",
                "kanban_board": 0,
                "organisation": 0,
                "organisation_note": 0,
                "project": 0,
                "project_note": 0,
                "request_for_change": 0,
                "requirement": 0,
                "requirement_item_note": 0,
                "requirement_note": 0,
                "schedule_object": 0,
                "sprint": 0,
                "task": 0,
                "tag": 0,
                "kanban_note": 0,
                "task_note": 0
            }
        ];



        // Tests
        expect(permissionStore._getMaximumFieldValue("fake_field")).toBe(0);
    })

    test("Permission Data with variation number 1", async () => {
        const permissionStore = usePermissionStore();

        // Set the data
        permissionStore.permissionData = [
            {
                "administration_assign_user_to_group": 4,
                "administration_create_group": 4,
                "administration_create_permission_set": 4,
                "administration_create_user": 4,
                "customer": 4,
                "document": 1,
                "group_id": 1,
                "group_name": "Administration",
                "kanban_board": 4,
                "organisation": 4,
                "organisation_note": 1,
                "project": 4,
                "project_note": 1,
                "request_for_change": 4,
                "requirement": 4,
                "requirement_item_note": 1,
                "requirement_note": 1,
                "schedule_object": 4,
                "sprint": 1,
                "task": 4,
                "tag": 4,
                "kanban_note": 1,
                "task_note": 1
            },
            {
                "administration_assign_user_to_group": 0,
                "administration_create_group": 0,
                "administration_create_permission_set": 0,
                "administration_create_user": 0,
                "customer": 0,
                "document": 0,
                "group_id": 0,
                "group_name": "QA Team",
                "kanban_board": 0,
                "organisation": 0,
                "organisation_note": 0,
                "project": 0,
                "project_note": 0,
                "request_for_change": 0,
                "requirement": 0,
                "requirement_item_note": 0,
                "requirement_note": 0,
                "schedule_object": 0,
                "sprint": 0,
                "task": 0,
                "tag": 0,
                "kanban_note": 0,
                "task_note": 0
            }
        ];



        // Tests
        expect(permissionStore._getMaximumFieldValue("administration_assign_user_to_group")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("administration_create_group")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("administration_create_permission_set")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("administration_create_user")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("customer")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("document")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("group_name")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("kanban_board")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("organisation")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("organisation_note")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("project")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("project_note")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("request_for_change")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("requirement")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("requirement_item_note")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("requirement_note")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("schedule_object")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("sprint")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("task")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("tag")).toBe(4);
        expect(permissionStore._getMaximumFieldValue("kanban_note")).toBe(1);
        expect(permissionStore._getMaximumFieldValue("task_note")).toBe(1);
    })


    test("Permission Data with variation number 2", async () => {
        const permissionStore = usePermissionStore();

        // Set the data
        permissionStore.permissionData = [
            {
                "administration_assign_user_to_group": 3,
                "administration_create_group": 3,
                "administration_create_permission_set": 3,
                "administration_create_user": 3,
                "customer": 3,
                "document": 0,
                "group_id": 0,
                "group_name": "Administration",
                "kanban_board": 3,
                "organisation": 3,
                "organisation_note": 0,
                "project": 3,
                "project_note": 0,
                "request_for_change": 3,
                "requirement": 3,
                "requirement_item_note": 0,
                "requirement_note": 0,
                "schedule_object": 3,
                "sprint": 0,
                "task": 3,
                "tag": 3,
                "kanban_note": 0,
                "task_note": 0
            },
            {
                "administration_assign_user_to_group": 0,
                "administration_create_group": 0,
                "administration_create_permission_set": 0,
                "administration_create_user": 0,
                "customer": 0,
                "document": 0,
                "group_id": 0,
                "group_name": "QA Team",
                "kanban_board": 0,
                "organisation": 0,
                "organisation_note": 0,
                "project": 0,
                "project_note": 0,
                "request_for_change": 0,
                "requirement": 0,
                "requirement_item_note": 0,
                "requirement_note": 0,
                "schedule_object": 0,
                "sprint": 0,
                "task": 0,
                "tag": 0,
                "kanban_note": 0,
                "task_note": 0
            }
        ];



        // Tests
        expect(permissionStore._getMaximumFieldValue("administration_assign_user_to_group")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("administration_create_group")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("administration_create_permission_set")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("administration_create_user")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("customer")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("document")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("group_name")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("kanban_board")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("organisation")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("organisation_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("project")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("project_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("request_for_change")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("requirement")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("requirement_item_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("schedule_object")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("sprint")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("task")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("tag")).toBe(3);
        expect(permissionStore._getMaximumFieldValue("kanban_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("task_note")).toBe(0);
    })



    test("Permission Data with variation number 3", async () => {
        const permissionStore = usePermissionStore();

        // Set the data
        permissionStore.permissionData = [
            {
                "administration_assign_user_to_group": 0,
                "administration_create_group": 0,
                "administration_create_permission_set": 0,
                "administration_create_user": 0,
                "customer": 0,
                "document": 0,
                "group_id": 0,
                "group_name": "QA Team",
                "kanban_board": 0,
                "organisation": 0,
                "organisation_note": 0,
                "project": 0,
                "project_note": 0,
                "request_for_change": 0,
                "requirement": 0,
                "requirement_item_note": 0,
                "requirement_note": 0,
                "schedule_object": 0,
                "sprint": 0,
                "task": 0,
                "tag": 0,
                "kanban_note": 0,
                "task_note": 0
            }
        ];

        // Tests
        expect(permissionStore._getMaximumFieldValue("administration_assign_user_to_group")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("administration_create_group")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("administration_create_permission_set")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("administration_create_user")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("customer")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("document")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("group_name")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("kanban_board")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("organisation")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("organisation_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("project")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("project_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("request_for_change")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement_item_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("requirement_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("schedule_object")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("sprint")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("task")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("tag")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("kanban_note")).toBe(0);
        expect(permissionStore._getMaximumFieldValue("task_note")).toBe(0);
    });
})