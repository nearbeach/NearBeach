import { test, expect } from '@playwright/test';

//Check that the user is logged in
test("Make sure user is logged in", async({ page }) : Promise<void> => {
    await page.goto("localhost:8000");

    //Make sure we are on the login page
    await expect(page).toHaveTitle("NearBeach Dashboard");
});

const page_array = [
    {test:'Card Information 1',url :'http://localhost:8000/card_information/1/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/Kanban Admin Only.jpg'},
    {test:'Change Task Information 1',url :'http://localhost:8000/change_task_information/1/', page_title:'Change Task 1',page_heading:'Change Task - 1',screenshot_path:'./test-results/Change Task - 1.jpg'},
    {test:'Customer Information 1',url :'http://localhost:8000/customer_information/1/', page_title:'Customer Information 1',page_heading:'Customer Information',screenshot_path:'./test-results/Customer Information.jpg'},
    {test:'Group Information 1',url :'http://localhost:8000/group_information/1/', page_title:'Group Information 1',page_heading:'Group Information',screenshot_path:'./test-results/Group Information.jpg'},
    {test:'Kanban Information 1',url :'http://localhost:8000/kanban_information/1/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/Kanban Information.jpg'},
    {test:'Kanban Card Information 1',url :'http://localhost:8000/kanban_information/1/card/1/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/Kanban Admin Only.jpg'},
    {test:'Kanban Information Edit Board 1',url :'http://localhost:8000/kanban_information/1/edit_board/', page_title:'Kanban Information 1',page_heading:'Kanban Admin Only',screenshot_path:'./test-results/Kanban Admin Only.jpg'},
    {test:'New Group',url :'http://localhost:8000/new_group/', page_title:'New Group',page_heading:'New Group',screenshot_path:'./test-results/New Group.jpg'},
    {test:'New Kanban',url :'http://localhost:8000/new_kanban/', page_title:'New Kanban',page_heading:'New Kanban',screenshot_path:'./test-results/New Kanban.jpg'},
    {test:'New Organisation',url :'http://localhost:8000/new_organisation/', page_title:'New Organisation',page_heading:'New Organisation',screenshot_path:'./test-results/New Organisation.jpg'},
    {test:'New Permission Set',url :'http://localhost:8000/new_permission_set/', page_title:'New Permission Set',page_heading:'New Permission Set',screenshot_path:'./test-results/New Permission Set.jpg'},
    {test:'New Project',url :'http://localhost:8000/new_project/', page_title:'New Project',page_heading:'New Project',screenshot_path:'./test-results/New Project.jpg'},
    {test:'New Request for Change',url :'http://localhost:8000/new_request_for_change/', page_title:'New RFC',page_heading:'New Request for Change',screenshot_path:'./test-results/New Request for Change.jpg'},
    {test:'New Requirement',url :'http://localhost:8000/new_requirement/', page_title:'New Requirements',page_heading:'New Requirement',screenshot_path:'./test-results/New Requirement.jpg'},
    {test:'New Task',url :'http://localhost:8000/new_task/', page_title:'New Task',page_heading:'New Task',screenshot_path:'./test-results/New Task.jpg'},
    {test:'New User',url :'http://localhost:8000/new_user/', page_title:'New User',page_heading:'New User',screenshot_path:'./test-results/New User.jpg'},
    {test:'Organisation Information 1',url :'http://localhost:8000/organisation_information/1/', page_title:'Organisation Information 1',page_heading:'Organisation Information',screenshot_path:'./test-results/Organisation Information.jpg'},
    {test:'Permission Set Information 1',url :'http://localhost:8000/permission_set_information/1/', page_title:'Permission Set 1',page_heading:'Permission Information',screenshot_path:'./test-results/Permission Set Information.jpg'},
    {test:'Profile Information',url :'http://localhost:8000/profile_information/', page_title:'Profile Information',page_heading:'My Profile',screenshot_path:'./test-results/Profile Information.jpg'},
    {test:'Project Information 1',url :'http://localhost:8000/project_information/1/', page_title:'Project Information 1',page_heading:'Project Information',screenshot_path:'./test-results/Project Information.jpg'},
    {test:'Requirement Information 1',url :'http://localhost:8000/requirement_information/1/', page_title:'Requirement Information 1',page_heading:'Requirement Information',screenshot_path:'./test-results/Requirement Information.jpg'},
    {test:'Requirement Item Information 1',url :'http://localhost:8000/requirement_item_information/1/', page_title:'Requirement Item 1',page_heading:'Requirement Item Information',screenshot_path:'./test-results/Requirement Item Information.jpg'},
    {test:'RFC Information 1',url :'http://localhost:8000/rfc_information/1/', page_title:'RFC 1',page_heading:'Request for Change',screenshot_path:'./test-results/RFC Information.jpg'},
    {test:'Search',url :'http://localhost:8000/search/', page_title:'Search',page_heading:'Search',screenshot_path:'./test-results/Search.jpg'},
    {test:'Task Information 1',url :'http://localhost:8000/task_information/1/', page_title:'Task Information 1',page_heading:'Task Information',screenshot_path:'./test-results/Task Information.jpg'},
    {test:'User Information 1',url :'http://localhost:8000/user_information/1/', page_title:'User Information 1',page_heading:'User Information',screenshot_path:'./test-results/User Information.jpg'},
]
//Loop through page_array
page_array.forEach((row) => {
    test(row.test, async({ page }) : Promise<void> => {
        await page.goto(row.url);

        //Make sure we are on the correct page using the title
        await expect(page).toHaveTitle(row.page_title);

        //Make sure the VueJS loaded
        await expect(page.getByRole(
            "heading",
            { name: row.page_heading, exact: true }
        )).toBeVisible();

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
        //await expect(locator).not.toContainText('error');
        await expect(page.locator("#loader")).toHaveCount(0);

        //Take screenshot
        await page.screenshot({
            path: row.screenshot_path,
            fullPage: true,
        });
    });
});