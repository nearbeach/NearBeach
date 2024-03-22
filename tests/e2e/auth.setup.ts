import { test as setup } from '@playwright/test';

// Auth File location
// const authFile : string = "tests/.auth/user.json";

// User credentials
// const username : string = 'dark_admin';
// const password: string = 'Test1234$';

type credentialsType = {
	username: string,
	password: string,
	authFile: string,
};

const credentials : credentialsType[] = [
	{ username: 'admin', password: 'Test1234$', authFile: 'tests/.auth/admin.json' },
	{ username: 'dark_admin', password: 'Test1234$', authFile: 'tests/.auth/dark_admin.json' },
	{ username: 'team_leader', password: 'Test1234$', authFile: 'tests/.auth/team_leader.json' },
	{ username: 'team_member', password: 'Test1234$', authFile: 'tests/.auth/team_member.json' },
	{ username: 'read_only', password: 'Test1234$', authFile: 'tests/.auth/read_only.json' },
]


Promise.all(credentials.map(async (single : credentialsType) : Promise<void> => {
	setup(`Authenticate the user ${single.username}`, async ({ page }) : Promise<void> => {
	//Loop through the credentials list - and login
		// Go to login page
		await page.goto('http://localhost:8000/login');

		// Type in username and password
		await page.locator("#id_username").fill(single.username);
		await page.locator("#id_password").fill(single.password);

		// Sign in time
		await page.getByRole('button', { name: 'Login' }).click();

		// Wait for page to login and then save the cookies
		await page.waitForURL('http://localhost:8000/');
		await page.context().storageState({ path: single.authFile });
	});
}));
