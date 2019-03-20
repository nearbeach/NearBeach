#Import required libraries
from locust import HttpLocust, TaskSet, task
import getpass

#Request the username and password to login into NearBeach
username = input("\nPlease enter the username: ")
password = getpass.getpass("\nPlease enter the password: ")

#The tests
class WebsiteUserTests(TaskSet):
    #On start - log in using above credentials
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.post(
            "/login",
            {
                "username":username,
                "password":password
            }
        )

    #On stop - we want everyone to log off
    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.client.post("/logout")

    #The tasks/pages we are looking at.
    @task(1)
    def index(self):
        self.client.get("/dashboard")

    @task(1)
    def profile(self):
        self.client.get("/my_profile")

    @task(1)
    def new_project(self):
        self.client.get("/new_project")

    @task(1)
    def project_information(self):
        self.client.get("/project_information/1")

    @task(1)
    def task_information(self):
        self.client.get("/task_information/1")

    @task(1)
    def timelinke(self):
        self.client.get("/timeline")

    @task(1)
    def search(self):
        self.client.get("/search")

#Get locus to start
class WebsiteUser(HttpLocust):    
    task_set = WebsiteUserTests
    min_wait = 5000
    max_wait = 9000
