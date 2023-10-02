import { test as setup } from '@playwright/test';

// Auth File location
const authFile : string = "tests/.auth/user.json";

// User credentials
const username : string = 'dark_admin';
const password: string = 'Test1234$';

setup('authenticate', async ({ page }) : Promise<void> => {
	// Perform authentication steps. Replace these actions with your own.
	// Go to login page
	await page.goto('http://localhost:8000/login');

	// Type in username and password
	await page.locator("#id_username").fill(username);
	await page.locator("#id_password").fill(password);

	// Sign in time
	await page.getByRole('button', { name: 'Login' }).click();

	// Wait for page to login and then save the cookies
	await page.waitForURL('http://localhost:8000/');
	await page.context().storageState({ path: authFile });
});
