import { test, expect } from "@playwright/test";

//Log the user in
test.use({
    storageState: 'tests/.auth/team_leader.json',
});

//Check that the user is logged in
test("Checking Team Leader 403", async({ page }): Promise<void> => {
    await page.goto("localhost:8000");

    //Make sure we are on the dashboard page
    await expect(page).toHaveTitle("NearBeach Dashboard");
});

type PageArrayType = {
    test: string,
    url: string
}

const page_array : PageArrayType[] = [
    {test:'Team Leader - 403 - Card Information 1',url :'http://localhost:8000/card_information/1/'},
    {test:'Team Leader - 403 - Change Task Information 1',url :'http://localhost:8000/change_task_information/1/'},
    {test:'Team Leader - 403 - Diagnostic Information',url :'http://localhost:8000/diagnostic_information/'},
    {test:'Team Leader - 403 - Group Information 1',url :'http://localhost:8000/group_information/1/'},
    {test:'Team Leader - 403 - Kanban Information 1',url :'http://localhost:8000/kanban_information/1/'},
    {test:'Team Leader - 403 - Kanban Card Information 1',url :'http://localhost:8000/kanban_information/1/card/1/'},
    {test:'Team Leader - 403 - Kanban Information Edit Board 1',url :'http://localhost:8000/kanban_information/1/edit_board/'},
    {test:'Team Leader - 403 - New Group',url :'http://localhost:8000/new_group/'},
    {test:'Team Leader - 403 - New Notification',url :'http://localhost:8000/new_notification/'},
    {test:'Team Leader - 403 - New Permission Set',url :'http://localhost:8000/new_permission_set/'},
    {test:'Team Leader - 403 - New User',url :'http://localhost:8000/new_user/'},
    {test:'Team Leader - 403 - Notification Information',url :'http://localhost:8000/notification_information/1/'},
    {test:'Team Leader - 403 - Object Status Editor Requirements',url :'http://localhost:8000/object_status_information/requirement/'},
    {test:'Team Leader - 403 - Object Status Requirement Item',url :'http://localhost:8000/object_status_information/requirement_item/'},
    {test:'Team Leader - 403 - Object Status Project',url :'http://localhost:8000/object_status_information/project/'},
    {test:'Team Leader - 403 - Object Status Task',url :'http://localhost:8000/object_status_information/task/'},
    {test:'Team Leader - 403 - Object Status List',url :'http://localhost:8000/object_status_list/'},
    {test:'Team Leader - 403 - Permission Set Information 1',url :'http://localhost:8000/permission_set_information/1/'},
    {test:'Team Leader - 403 - Project Information 1',url :'http://localhost:8000/project_information/1/'},
    {test:'Team Leader - 403 - Requirement Information 1',url :'http://localhost:8000/requirement_information/1/'},
    {test:'Team Leader - 403 - Requirement Item Information 1',url :'http://localhost:8000/requirement_item_information/1/'},
    {test:'Team Leader - 403 - RFC Information 1',url :'http://localhost:8000/rfc_information/1/'},
    {test:'Team Leader - 403 - Sprint Information',url :'http://localhost:8000/sprint_information/1/'},
    {test:'Team Leader - 403 - Task Information 1',url :'http://localhost:8000/task_information/1/'},
    {test:'Team Leader - 403 - User Information 1',url :'http://localhost:8000/user_information/1/'},
]

//Loop through page_array
page_array.forEach((row : PageArrayType): void => {
    test(row.test, async({page}) : Promise<void> => {
        //Make sure there are 403 errors
        page.on("response", data => {
            if (data.url() === row.url) {
                if (data.ok()) {
                    test.info().annotations.push({
                        type: "Response Status is OK",
                        description: "User should not have any access to page",
                    });
                }
                if (data.status() !== 403) {
                    test.info().annotations.push({
                        type: "Status not 403",
                        description: `Url: ${data.url()} || Status: ${data.status()}`,
                    });
                }
                expect.soft(data.ok()).toBeFalsy();
            }
        });

        //Go to url
        await page.goto(row.url);
    });
});