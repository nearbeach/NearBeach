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
    {test:'Dark Mode Card Information 1',url :'http://localhost:8000/card_information/1/',screenshot_path:'./test-results/Kanban Admin Only dark.jpg'},
    {test:'Dark Mode Change Task Information 1',url :'http://localhost:8000/change_task_information/1/',screenshot_path:'./test-results/Change Task - 1 dark.jpg'},
    {test:'Dark Mode Customer Information 1',url :'http://localhost:8000/customer_information/1/',screenshot_path:'./test-results/Customer Information dark.jpg'},
    {test:'Dark Mode Group Information 1',url :'http://localhost:8000/group_information/1/',screenshot_path:'./test-results/Group Information dark.jpg'},
    {test:'Dark Mode Kanban Information 1',url :'http://localhost:8000/kanban_information/1/',screenshot_path:'./test-results/Kanban Information dark.jpg'},
    {test:'Dark Mode Kanban Card Information 1',url :'http://localhost:8000/kanban_information/1/card/1/',screenshot_path:'./test-results/Kanban Admin Only dark.jpg'},
    {test:'Dark Mode Kanban Information Edit Board 1',url :'http://localhost:8000/kanban_information/1/edit_board/',screenshot_path:'./test-results/Kanban Edit Board dark.jpg'},
    {test:'Dark Mode New Group',url :'http://localhost:8000/new_group/',screenshot_path:'./test-results/New Group dark.jpg'},
    {test:'Dark Mode New Kanban',url :'http://localhost:8000/new_kanban/',screenshot_path:'./test-results/New Kanban dark.jpg'},
    {test:'Dark Mode New Organisation',url :'http://localhost:8000/new_organisation/',screenshot_path:'./test-results/New Organisation dark.jpg'},
    {test:'Dark Mode New Permission Set',url :'http://localhost:8000/new_permission_set/',screenshot_path:'./test-results/New Permission Set dark.jpg'},
    {test:'Dark Mode New Project',url :'http://localhost:8000/new_project/',screenshot_path:'./test-results/New Project dark.jpg'},
    {test:'Dark Mode New Request for Change',url :'http://localhost:8000/new_request_for_change/',screenshot_path:'./test-results/New Request for Change dark.jpg'},
    {test:'Dark Mode New Requirement',url :'http://localhost:8000/new_requirement/',screenshot_path:'./test-results/New Requirement dark.jpg'},
    {test:'Dark Mode New Task',url :'http://localhost:8000/new_task/',screenshot_path:'./test-results/New Task dark.jpg'},
    {test:'Dark Mode New User',url :'http://localhost:8000/new_user/',screenshot_path:'./test-results/New User dark.jpg'},
    {test:'Dark Mode Organisation Information 1',url :'http://localhost:8000/organisation_information/1/',screenshot_path:'./test-results/Organisation Information dark.jpg'},
    {test:'Dark Mode Permission Set Information 1',url :'http://localhost:8000/permission_set_information/1/',screenshot_path:'./test-results/Permission Set Information dark.jpg'},
    {test:'Dark Mode Profile Information',url :'http://localhost:8000/profile_information/',screenshot_path:'./test-results/Profile Information dark.jpg'},
    {test:'Dark Mode Project Information 1',url :'http://localhost:8000/project_information/1/',screenshot_path:'./test-results/Project Information dark.jpg'},
    {test:'Dark Mode Requirement Information 1',url :'http://localhost:8000/requirement_information/1/',screenshot_path:'./test-results/Requirement Information dark.jpg'},
    {test:'Dark Mode Requirement Item Information 1',url :'http://localhost:8000/requirement_item_information/1/',screenshot_path:'./test-results/Requirement Item Information dark.jpg'},
    {test:'Dark Mode RFC Information 1',url :'http://localhost:8000/rfc_information/1/',screenshot_path:'./test-results/RFC Information dark.jpg'},
    {test:'Dark Mode Search',url :'http://localhost:8000/search/',screenshot_path:'./test-results/Search dark.jpg'},
    {test:'Dark Mode Task Information 1',url :'http://localhost:8000/task_information/1/',screenshot_path:'./test-results/Task Information dark.jpg'},
    {test:'Dark Mode User Information 1',url :'http://localhost:8000/user_information/1/',screenshot_path:'./test-results/User Information dark.jpg'},
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