import { test, expect } from '@playwright/test';

//Log the user in
test.use({
    storageState: 'tests/.auth/dark_admin.json',
});

//Check that the user is logged in
test("Checking out Dark Mode", async({ page }) : Promise<void> => {
    await page.goto("localhost:8000");

    //Make sure we are on the login page
    await expect(page).toHaveTitle("NearBeach Dashboard");
});

type PageArrayType = {
    test: string
    url: string,
    screenshot_path: string,
};
const page_array : PageArrayType[] = [
    {test:'Dark Admin - Card Information 1',url :'http://localhost:8000/card_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Kanban Admin Only.jpg'},
    {test:'Dark Admin - Change Task Information 1',url :'http://localhost:8000/change_task_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Change Task - 1.jpg'},
    {test:'Dark Admin - Customer Information 1',url :'http://localhost:8000/customer_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Customer Information.jpg'},
    {test:'Dark Admin - Diagnostic Information',url :'http://localhost:8000/diagnostic_information/',screenshot_path:'./test-results/shakeout/dark-admin/Diagnostic Information.jpg'},
    {test:'Dark Admin - Group Information 1',url :'http://localhost:8000/group_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Group Information.jpg'},
    {test:'Dark Admin - Kanban Information 1',url :'http://localhost:8000/kanban_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Kanban Information.jpg'},
    {test:'Dark Admin - Kanban Card Information 1',url :'http://localhost:8000/kanban_information/1/card/1/',screenshot_path:'./test-results/shakeout/dark-admin/Kanban Admin Only.jpg'},
    {test:'Dark Admin - Kanban Information Edit Board 1',url :'http://localhost:8000/kanban_information/1/edit_board/',screenshot_path:'./test-results/shakeout/dark-admin/Kanban Edit Board.jpg'},
    {test:'Dark Admin - New Group',url :'http://localhost:8000/new_group/',screenshot_path:'./test-results/shakeout/dark-admin/New Group.jpg'},
    {test:'Dark Admin - New Kanban',url :'http://localhost:8000/new_kanban/',screenshot_path:'./test-results/shakeout/dark-admin/New Kanban.jpg'},
    {test:'Dark Admin - New Notification',url :'http://localhost:8000/new_notification/',screenshot_path:'./test-results/shakeout/dark-admin/New Notification.jpg'},
    {test:'Dark Admin - New Organisation',url :'http://localhost:8000/new_organisation/',screenshot_path:'./test-results/shakeout/dark-admin/New Organisation.jpg'},
    {test:'Dark Admin - New Permission Set',url :'http://localhost:8000/new_permission_set/',screenshot_path:'./test-results/shakeout/dark-admin/New Permission Set.jpg'},
    {test:'Dark Admin - New Project',url :'http://localhost:8000/new_project/',screenshot_path:'./test-results/shakeout/dark-admin/New Project.jpg'},
    {test:'Dark Admin - New Request for Change',url :'http://localhost:8000/new_request_for_change/',screenshot_path:'./test-results/shakeout/dark-admin/New Request for Change.jpg'},
    {test:'Dark Admin - New Requirement',url :'http://localhost:8000/new_requirement/',screenshot_path:'./test-results/shakeout/dark-admin/New Requirement.jpg'},
    {test:'Dark Admin - New Task',url :'http://localhost:8000/new_task/',screenshot_path:'./test-results/shakeout/dark-admin/New Task.jpg'},
    {test:'Dark Admin - New User',url :'http://localhost:8000/new_user/',screenshot_path:'./test-results/shakeout/dark-admin/New User.jpg'},
    {test:'Dark Admin - Notification Information',url :'http://localhost:8000/notification_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Notification Information.jpg'},
    {test:'Dark Admin - Object Status Editor Requirements',url :'http://localhost:8000/object_status_information/requirement/',screenshot_path:'./test-results/shakeout/dark-admin/Requirement Status Editor.jpg'},
    {test:'Dark Admin - Object Status Requirement Item',url :'http://localhost:8000/object_status_information/requirement_item/',screenshot_path:'./test-results/shakeout/dark-admin/Requirement Item Status Editor.jpg'},
    {test:'Dark Admin - Object Status Project',url :'http://localhost:8000/object_status_information/project/',screenshot_path:'./test-results/shakeout/dark-admin/Project Status Editor.jpg'},
    {test:'Dark Admin - Object Status Task',url :'http://localhost:8000/object_status_information/task/',screenshot_path:'./test-results/shakeout/dark-admin/Task Status Editor.jpg'},
    {test:'Dark Admin - Object Status List',url :'http://localhost:8000/object_status_list/',screenshot_path:'./test-results/shakeout/dark-admin/Object Status List Information.jpg'},
    {test:'Dark Admin - Organisation Information 1',url :'http://localhost:8000/organisation_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Organisation Information.jpg'},
    {test:'Dark Admin - Permission Set Information 1',url :'http://localhost:8000/permission_set_information/1/', screenshot_path:'./test-results/shakeout/dark-admin/Permission Set Information.jpg'},
    {test:'Dark Admin - Profile Information',url :'http://localhost:8000/profile_information/',screenshot_path:'./test-results/shakeout/dark-admin/Profile Information.jpg'},
    {test:'Dark Admin - Project Information 1',url :'http://localhost:8000/project_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Project Information.jpg'},
    {test:'Dark Admin - Requirement Information 1',url :'http://localhost:8000/requirement_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Requirement Information.jpg'},
    {test:'Dark Admin - Requirement Item Information 1',url :'http://localhost:8000/requirement_item_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Requirement Item Information.jpg'},
    {test:'Dark Admin - RFC Information 1',url :'http://localhost:8000/rfc_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/RFC Information.jpg'},
    {test:'Dark Admin - Search',url :'http://localhost:8000/search/',screenshot_path:'./test-results/shakeout/dark-admin/Search.jpg'},
    {test:'Dark Admin - Search Notifications',url :'http://localhost:8000/search/notification/',screenshot_path:'./test-results/shakeout/dark-admin/Search Notifications.jpg'},
    {test:'Dark Admin - Search Sprint',url :'http://localhost:8000/search/sprint/',screenshot_path:'./test-results/shakeout/team-leader/Search Sprint.jpg'},
    {test:'Dark Admin - Sprint Information',url :'http://localhost:8000/sprint_information/1/',screenshot_path:'./test-results/shakeout/team-leader/Sprint Information 2.jpg'},
    {test:'Dark Admin - Task Information 1',url :'http://localhost:8000/task_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/Task Information.jpg'},
    {test:'Dark Admin - User Information 1',url :'http://localhost:8000/user_information/1/',screenshot_path:'./test-results/shakeout/dark-admin/User Information.jpg'},
];

page_array.forEach((row : PageArrayType) => {
    test(row.test, async({ page }) : Promise<void> => {
        await page.goto(row.url);

        //await expect(locator).not.toContainText('error');
        await expect(page.locator("#loader")).toHaveCount(0);

        //Take screenshot
        await page.screenshot({
            path: row.screenshot_path,
            fullPage: true,
        });
    });
});