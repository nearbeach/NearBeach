from collections import namedtuple
from django.test import TestCase, Client
from django.urls import reverse

# Declaration of Username and Password
username = "team_leader"
password = "Test1234$"


def login_user(c: object, self: object) -> object:
    response = c.post(
        reverse("login"),
        self.credentials,
        follow=True,
    )
    self.assertTrue(response.context["user"].is_active)


class TeamLeaderPermissionTests(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        # Login
        self.credentials = {"username": username, "password": password}
        
        # Setup the client
        self.client = Client()

    
    # def test_dashboard_loads_successful(self):
    #     '''
    #     Make sure the dashboard will load for the user
    #     '''
    #     response = self.client.get(reverse('dashboard', args=[]), {})
    #     self.assertEqual(response.status_code, 302) 


    def test_basic_page_loads_successful(self):
        '''
        The following tests will make sure the team leader can access most pages on the
        system. This is only testing pages they can LAND on.
        '''
        # urlObject = namedtuple('url','arguments','form_data','response_status_code', defaults=['/',[],{},302])
        URLTest = namedtuple('URLTest', ['url', 'args', 'data', 'status_code'], defaults=["", [], {}, 200])

        data_list = [
            URLTest('dashboard',[],{},302),
            URLTest('change_task_information',[2],{},302),
            URLTest('customer_information',[2],{},302),
            URLTest('kanban_information',[2],{},302),
            URLTest('permission_set_information',[2],{},302),
            URLTest('profile_information',[],{},302),
            URLTest('new_customer',[],{},302),
            URLTest('new_group',[],{},302),
            URLTest('new_kanban',[],{},302),
            URLTest('new_organisation',[],{},302),
            URLTest('new_permission_set',[],{},302),
            URLTest('new_project',[],{},302),
            URLTest('new_request_for_change',[],{},302),
            URLTest('new_requirement',[],{},302),
            URLTest('new_task',[],{},302),
            URLTest('new_user',[],{},302),
            URLTest('organisation_information',[2],{},302),
            URLTest('project_information',[2],{},302),
            URLTest('requirement_information',[2],{},302),
            URLTest('requirement_item_information',[2],{},302),
            URLTest('rfc_information',[2],{},302),
            URLTest('rfc_readonly',[2],{},302),
            URLTest('search',[],{},302),
            URLTest('search_group',[],{},302),
            URLTest('search_customer',[],{},302),
            URLTest('search_organisation',[],{},302),
            URLTest('search_permission_set',[],{},302),
            URLTest('search_tag',[],{},302),
            URLTest('search_user',[],{},302),
            URLTest('task_information',[2],{},302),
            URLTest('user_information',[2],{},302),
        ]

        # Loop through each url to test to make sure the decorator is applied
        for data in data_list:
            with self.subTest(data):
                response = self.client.get(reverse(data.url, args=data.args), data.data)
                #response = c.post(reverse(data['url'], args=["task", 1]), data['formData'])
                self.assertEqual(response.status_code, data.status_code)
