from selenium import webdriver

import json
import time

# Get login details
with open('config.py') as json_file:
    login_data = json.load(json_file)

desired_cap = {
    'browser': 'Edge',
    'browser_version': '80.0',
    'os': 'Windows',
    'os_version': '10',
    'resolution': '1024x768',
    'name': 'Shakeout Testing for Windows 10 Edge'
}


driver = webdriver.Remote(
    command_executor=
    f"http://{login_data['browserstack_username']}:{login_data['browserstack_apikey']}@hub.browserstack.com:80/wd/hub",
    desired_capabilities=desired_cap)

# Loads the login page for NearBeach
driver.get("http://test.nearbeach.org")

# Make sure we are on the NearBeach Screen
if not "NearBeach Login Screen" in driver.title:
    raise Exception("Unable to load NearBeach Login Screen!")

# Save Login Screenshot
driver.save_screenshot('login_screen.png')

# Time to log into NearBeach
driver.find_element_by_id("id_username").send_keys(
    login_data['login']['administrator']['username'])
driver.find_element_by_id("id_password").send_keys(
    login_data['login']['administrator']['password'])
driver.find_element_by_id("id_password").submit()

time.sleep(5)  # Sleep to allow login
# Save Login Screenshot
driver.save_screenshot('dashboard.png')


print(driver.title)
driver.quit()
