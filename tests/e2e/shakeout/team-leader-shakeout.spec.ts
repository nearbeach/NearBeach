import { test, expect } from '@playwright/test';

//Log the user in
test.use({
    storageState: 'tests/.auth/team_leader.json',
});

//Check that the user is logged in
test("Checking Team Leader Shakeout", async({ page }) : Promise<void> => {
    await page.goto("localhost:8000");

    //Make sure we are on the dashboard page
    await expect(page).toHaveTitle("NearBeach Dashboard");
});

type PageArrayType = {
    test: string
    url: string,
    screenshot_path: string,
};
const page_array : PageArrayType[] = [
    {test:'Team Leader - Card Information 2',url :'http://localhost:8000/card_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Kanban Admin Only.jpg'},
    {test:'Team Leader - Change Task Information 2',url :'http://localhost:8000/change_task_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Change Task - 1.jpg'},
    {test:'Team Leader - Customer Information 1',url :'http://localhost:8000/customer_information/1/',screenshot_path:'./test-results/shakeout/team-leader/Customer Information.jpg'},
    {test:'Team Leader - Kanban Information 2',url :'http://localhost:8000/kanban_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Kanban Information.jpg'},
    {test:'Team Leader - Kanban Card Information 2',url :'http://localhost:8000/kanban_information/2/card/2/',screenshot_path:'./test-results/shakeout/team-leader/Kanban Admin Only.jpg'},
    {test:'Team Leader - Kanban Information Edit Board 2',url :'http://localhost:8000/kanban_information/2/edit_board/',screenshot_path:'./test-results/shakeout/team-leader/Kanban Edit Board.jpg'},
    {test:'Team Leader - New Kanban',url :'http://localhost:8000/new_kanban/',screenshot_path:'./test-results/shakeout/team-leader/New Kanban.jpg'},
    {test:'Team Leader - New Organisation',url :'http://localhost:8000/new_organisation/',screenshot_path:'./test-results/shakeout/team-leader/New Organisation.jpg'},
    {test:'Team Leader - New Project',url :'http://localhost:8000/new_project/',screenshot_path:'./test-results/shakeout/team-leader/New Project.jpg'},
    {test:'Team Leader - New Request for Change',url :'http://localhost:8000/new_request_for_change/',screenshot_path:'./test-results/shakeout/team-leader/New Request for Change.jpg'},
    {test:'Team Leader - New Requirement',url :'http://localhost:8000/new_requirement/',screenshot_path:'./test-results/shakeout/team-leader/New Requirement.jpg'},
    {test:'Team Leader - New Task',url :'http://localhost:8000/new_task/',screenshot_path:'./test-results/shakeout/team-leader/New Task.jpg'},
    {test:'Team Leader - Organisation Information 1',url :'http://localhost:8000/organisation_information/1/',screenshot_path:'./test-results/shakeout/team-leader/Organisation Information.jpg'},
    {test:'Team Leader - Profile Information',url :'http://localhost:8000/profile_information/',screenshot_path:'./test-results/shakeout/team-leader/Profile Information.jpg'},
    {test:'Team Leader - Project Information 2',url :'http://localhost:8000/project_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Project Information.jpg'},
    {test:'Team Leader - Requirement Information 2',url :'http://localhost:8000/requirement_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Requirement Information.jpg'},
    {test:'Team Leader - Requirement Item Information 2',url :'http://localhost:8000/requirement_item_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Requirement Item Information.jpg'},
    {test:'Team Leader - RFC Information 2',url :'http://localhost:8000/rfc_information/2/',screenshot_path:'./test-results/shakeout/team-leader/RFC Information.jpg'},
    {test:'Team Leader - Search',url :'http://localhost:8000/search/',screenshot_path:'./test-results/shakeout/team-leader/Search.jpg'},
    {test:'Team Leader - Search Sprint',url :'http://localhost:8000/search/sprint/',screenshot_path:'./test-results/shakeout/team-leader/Search Sprint.jpg'},
    {test:'Team Leader - Sprint Information',url :'http://localhost:8000/sprint_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Sprint Information 2.jpg'},
    {test:'Team Leader - Task Information 2',url :'http://localhost:8000/task_information/2/',screenshot_path:'./test-results/shakeout/team-leader/Task Information.jpg'},
];

page_array.forEach((row : PageArrayType) => {
    test(row.test, async({ page }) : Promise<void> => {
        //Make sure there are no errors in the console
        page.on("console", message => {
            if (message.type() === "error") {
                test.info().annotations.push({
                    type: 'Console Errors',
                    description: message.text()
                });
            }
            expect.soft(message.type()).not.toBe("error");
        });

        //Make sure there are no warnings in the console
        page.on("console", message => {
            if (message.type() === "warning") {
                test.info().annotations.push({
                    type: 'Console Warnings',
                    description: message.text()
                });
            }
            expect.soft(message.type()).not.toBe("warning");
        });

        //RESPONSE
        page.on("response", data => {
            if (!data.ok()) {
                test.info().annotations.push({
                    type: "Response Status",
                    description:
                        `Url: ${data.url()} || Status Code: ${data.status()} || Status Text: ${data.statusText()}`,
                });
            }

            //If the status range is between 200-299, OR any of the following status 301, 302, 307
            const condition1: boolean = data.ok();
            const condition2: boolean = [301, 302, 307].includes(data.status())
            expect.soft(condition1 || condition2).toBeTruthy();
        });

        //Go to the page
        await page.goto(row.url);

        //await expect(locator).not.toContainText('error');
        await expect(page.locator("#loader")).toHaveCount(0);

        //Take screenshot
        await page.screenshot({
            path: row.screenshot_path,
            fullPage: true,
        });
    });
});