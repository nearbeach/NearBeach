# Import the locust libraries
import time, getpass
from locust import HttpUser, task, between

#Request the username and password to login into NearBeach
username = input("\nPlease enter the username: ")
password = getpass.getpass("\nPlease enter the password: ")

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.post("/login", json={"id_username": username, "id_password": password})

    @task
    def dashboard(self):
        self.client.get("/")
       

    @task(3)
    def requirement_information(self):
        for item_id in range(10):
            self.client.get(f"/requirement_information/1")



