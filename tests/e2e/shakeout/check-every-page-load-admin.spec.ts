import { test, expect } from '@playwright/test';

//Log the user in
test.use({
    storageState: 'tests/.auth/admin.json',
});

//Check that the user is logged in
test("Make sure user is logged in", async({ page }) : Promise<void> => {
    await page.goto("localhost:8000");

    //Make sure we are on the login page
    await expect(page).toHaveTitle("NearBeach Dashboard");
});

const page_array = [
    {test:'Admin - Card Information 1',url :'http://localhost:8000/card_information/1/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/shakeout/admin/Kanban Admin Only.jpg'},
    {test:'Admin - Change Task Information 1',url :'http://localhost:8000/change_task_information/1/', page_title:'Change Task 1',page_heading:'Change Task - 1',screenshot_path:'./test-results/shakeout/admin/Change Task - 1.jpg'},
    {test:'Admin - Customer Information 1',url :'http://localhost:8000/customer_information/1/', page_title:'Customer Information 1',page_heading:'Customer Information',screenshot_path:'./test-results/shakeout/admin/Customer Information.jpg'},
    {test:'Admin - Diagnostic Information',url :'http://localhost:8000/diagnostic_information/', page_title:'Diagnostic Information',page_heading:'Diagnostic Information',screenshot_path:'./test-results/shakeout/admin/Diagnostic Information.jpg'},
    {test:'Admin - Group Information 1',url :'http://localhost:8000/group_information/1/', page_title:'Group Information 1',page_heading:'Group Information',screenshot_path:'./test-results/shakeout/admin/Group Information.jpg'},
    {test:'Admin - Kanban Information 1',url :'http://localhost:8000/kanban_information/1/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/shakeout/admin/Kanban Information.jpg'},
    {test:'Admin - Kanban Card Information 1',url :'http://localhost:8000/kanban_information/1/card/1/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/shakeout/admin/Kanban Admin Only.jpg'},
    {test:'Admin - Kanban Information Edit Board 1',url :'http://localhost:8000/kanban_information/1/edit_board/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/shakeout/admin/Kanban Edit Board.jpg'},
    {test:'Admin - New Group',url :'http://localhost:8000/new_group/', page_title:'New Group',page_heading:'New Group',screenshot_path:'./test-results/shakeout/admin/New Group.jpg'},
    {test:'Admin - New Kanban',url :'http://localhost:8000/new_kanban/', page_title:'New Kanban',page_heading:'New Kanban',screenshot_path:'./test-results/shakeout/admin/New Kanban.jpg'},
    {test:'Admin - New Notification',url :'http://localhost:8000/new_notification/', page_title:'New Notification',page_heading:'New Notification',screenshot_path:'./test-results/shakeout/admin/New Notification.jpg'},
    {test:'Admin - New Organisation',url :'http://localhost:8000/new_organisation/', page_title:'New Organisation',page_heading:'New Organisation',screenshot_path:'./test-results/shakeout/admin/New Organisation.jpg'},
    {test:'Admin - New Permission Set',url :'http://localhost:8000/new_permission_set/', page_title:'New Permission Set',page_heading:'New Permission Set',screenshot_path:'./test-results/shakeout/admin/New Permission Set.jpg'},
    {test:'Admin - New Project',url :'http://localhost:8000/new_project/', page_title:'New Project',page_heading:'New Project',screenshot_path:'./test-results/shakeout/admin/New Project.jpg'},
    {test:'Admin - New Request for Change',url :'http://localhost:8000/new_request_for_change/', page_title:'New RFC',page_heading:'New Request for Change',screenshot_path:'./test-results/shakeout/admin/New Request for Change.jpg'},
    {test:'Admin - New Requirement',url :'http://localhost:8000/new_requirement/', page_title:'New Requirements',page_heading:'New Requirement',screenshot_path:'./test-results/shakeout/admin/New Requirement.jpg'},
    {test:'Admin - New Task',url :'http://localhost:8000/new_task/', page_title:'New Task',page_heading:'New Task',screenshot_path:'./test-results/shakeout/admin/New Task.jpg'},
    {test:'Admin - New User',url :'http://localhost:8000/new_user/', page_title:'New User',page_heading:'New User',screenshot_path:'./test-results/shakeout/admin/New User.jpg'},
    {test:'Admin - Notification Information',url :'http://localhost:8000/notification_information/1/', page_title:'Notification 1',page_heading:'Notification Information',screenshot_path:'./test-results/shakeout/admin/Notification Information.jpg'},
    {test:'Admin - Object Status Editor Requirements',url :'http://localhost:8000/object_status_information/requirement/', page_title:'Requirement Status Editor',page_heading:'Requirement Status Editor',screenshot_path:'./test-results/shakeout/admin/Requirement Status Editor.jpg'},
    {test:'Admin - Object Status Requirement Item',url :'http://localhost:8000/object_status_information/requirement_item/', page_title:'Requirement Item Status Editor',page_heading:'Requirement Item Status Editor',screenshot_path:'./test-results/shakeout/admin/Requirement Item Status Editor.jpg'},
    {test:'Admin - Object Status Project',url :'http://localhost:8000/object_status_information/project/', page_title:'Project Status Editor',page_heading:'Project Status Editor',screenshot_path:'./test-results/shakeout/admin/Project Status Editor.jpg'},
    {test:'Admin - Object Status Task',url :'http://localhost:8000/object_status_information/task/', page_title:'Task Status Editor',page_heading:'Task Status Editor',screenshot_path:'./test-results/shakeout/admin/Task Status Editor.jpg'},
    {test:'Admin - Object Status List',url :'http://localhost:8000/object_status_list/', page_title:'Object Status List',page_heading:'Object Status List',screenshot_path:'./test-results/shakeout/admin/Object Status List Information.jpg'},
    {test:'Admin - Organisation Information 1',url :'http://localhost:8000/organisation_information/1/', page_title:'Organisation Information 1',page_heading:'Organisation Information',screenshot_path:'./test-results/shakeout/admin/Organisation Information.jpg'},
    {test:'Admin - Permission Set Information 1',url :'http://localhost:8000/permission_set_information/1/', page_title:'Permission Set 1',page_heading:'Permission Information',screenshot_path:'./test-results/shakeout/admin/Permission Set Information.jpg'},
    {test:'Admin - Profile Information',url :'http://localhost:8000/profile_information/', page_title:'Profile Information',page_heading:'My Profile',screenshot_path:'./test-results/shakeout/admin/Profile Information.jpg'},
    {test:'Admin - Project Information 1',url :'http://localhost:8000/project_information/1/', page_title:'Project Information 1',page_heading:'Project Information',screenshot_path:'./test-results/shakeout/admin/Project Information.jpg'},
    {test:'Admin - Requirement Information 1',url :'http://localhost:8000/requirement_information/1/', page_title:'Requirement Information 1',page_heading:'Requirement Information',screenshot_path:'./test-results/shakeout/admin/Requirement Information.jpg'},
    {test:'Admin - Requirement Item Information 1',url :'http://localhost:8000/requirement_item_information/1/', page_title:'Requirement Item 1',page_heading:'Requirement Item Information',screenshot_path:'./test-results/shakeout/admin/Requirement Item Information.jpg'},
    {test:'Admin - RFC Information 1',url :'http://localhost:8000/rfc_information/1/', page_title:'RFC 1',page_heading:'Request for Change',screenshot_path:'./test-results/shakeout/admin/RFC Information.jpg'},
    {test:'Admin - Search',url :'http://localhost:8000/search/', page_title:'Search',page_heading:'Search',screenshot_path:'./test-results/shakeout/admin/Search.jpg'},
    {test:'Admin - Search Notifications',url :'http://localhost:8000/search/notification/', page_title:'Search Notifications',page_heading:'Search Notifications',screenshot_path:'./test-results/shakeout/admin/Search Notifications.jpg'},
    {test:'Admin - Search Sprint',url :'http://localhost:8000/search/sprint/', page_title: "Search Sprints", page_heading: "Search Sprints", screenshot_path:'./test-results/shakeout/team-leader/Search Sprint.jpg'},
    {test:'Admin - Sprint Information',url :'http://localhost:8000/sprint_information/1/', page_title: "Sprint Information 1", page_heading: "project-1 - Sprint 1 - 18 Mar 2024", screenshot_path:'./test-results/shakeout/team-leader/Sprint Information 2.jpg'},
    {test:'Admin - Task Information 1',url :'http://localhost:8000/task_information/1/', page_title:'Task Information 1',page_heading:'Task Information',screenshot_path:'./test-results/shakeout/admin/Task Information.jpg'},
    {test:'Admin - User Information 1',url :'http://localhost:8000/user_information/1/', page_title:'User Information 1',page_heading:'User Information',screenshot_path:'./test-results/shakeout/admin/User Information.jpg'},
    {test:'Admin - Scheduled Objects',url :'http://localhost:8000/scheduled_objects/', page_title:'Scheduled Objects',page_heading:'Scheduled Objects',screenshot_path:'./test-results/shakeout/admin/Scheduled Objects.jpg'},
    {test:'Admin - Scheduled Objects 1',url:'http://localhost:8000/scheduled_object_information/1/', page_title:'Scheduled Object 1',page_heading: 'Scheduled Object Information', screenshot_path: './test-results/shakeout/admin/Scheduled Objects 1.jpg'},
]

//Loop through page_array
page_array.forEach((row) => {
    test(row.test, async({ page }) : Promise<void> => {
        //Make sure there are no errors in the console
        page.on(
            "console",
            message => {
                if (message.type() === "error") {
                    test.info().annotations.push({
                        type: 'Console Errors',
                        description: message.text()
                    });
                }
                expect(message.type()).not.toBe("error");
            }
        );

        //Make sure there are no warnings in the console
        page.on(
            "console",
            message => {
                if (message.type() === "warning") {
                    test.info().annotations.push({
                        type: 'Console Warnings',
                        description: message.text()
                    });
                }
                expect(message.type()).not.toBe("warning");
            }
        );

        await page.goto(row.url);

        //Make sure we are on the correct page using the title
        await expect(page).toHaveTitle(row.page_title);

        //Make sure the VueJS loaded
        await expect(page.getByRole(
            "heading",
            { name: row.page_heading, exact: true }
        )).toBeVisible();

        //await expect(locator).not.toContainText('error');
        await expect(page.locator("#loader")).toHaveCount(0);

        //Take screenshot
        await page.screenshot({
            path: row.screenshot_path,
            fullPage: true,
        });
    });
});