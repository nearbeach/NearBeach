"""Services that no api route reaches yet (organisation, customer, sprint) - tested by calling them directly,
so they are known to work before a view is put in front of them."""
from types import SimpleNamespace

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status

from NearBeach.models.customer import Customer
from NearBeach.models.organisation import Organisation
from NearBeach.models.sprint.sprint import Sprint
from NearBeach.serializers.sprint_link_serializer import SprintLinkSerializer
from NearBeach.services.customer.CustomerService import CustomerService
from NearBeach.services.organisation.OrganisationService import OrganisationService
from NearBeach.services.sprint.SprintObjectLinkService import SprintObjectLinkService
from NearBeach.services.sprint.SprintService import SprintService


class ServiceTestBase(TestCase):
    fixtures = ["NearBeach_basic_setup.json"]

    def setUp(self):
        self.user = User.objects.get(username="admin")

    def request(self, data=None, method="POST"):
        """The parts of a request the services read"""
        return SimpleNamespace(data=data or {}, user=self.user, method=method)


class OrganisationServiceTests(ServiceTestBase):
    service = OrganisationService(destination="organisation", location_id=1)
    body = {"name": "Acme", "website": "https://acme.example", "email": "hello@acme.example"}

    def test_create(self):
        data, http_status = self.service.create(self.request(self.body))

        self.assertEqual(http_status, status.HTTP_201_CREATED)
        self.assertEqual((data["name"], data["website"], data["email"]), ("Acme", "https://acme.example", "hello@acme.example"))
        self.assertTrue(Organisation.objects.filter(pk=data["id"], name="Acme", is_deleted=False).exists())

    def test_create_rejects_bad_input_and_saves_nothing(self):
        before = Organisation.objects.count()

        for name, body in {
            "empty": {},
            "no name": {**self.body, "name": ""},
            "bad email": {**self.body, "email": "not-an-email"},
            "bad website": {**self.body, "website": "not a url"},
        }.items():
            with self.subTest(name):
                _, http_status = self.service.create(self.request(body))

                self.assertEqual(http_status, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Organisation.objects.count(), before)

    # def test_update_changes_only_what_was_sent(self):
    #     organisation = Organisation.objects.get(pk=1)
    #     email = organisation.email
    #
    #     data, http_status = self.service.update(self.request({"name": "Renamed"}, "PATCH"), None)
    #
    #     self.assertEqual(http_status, status.HTTP_200_OK)
    #     self.assertEqual(data["name"], "Renamed")
    #     organisation.refresh_from_db()
    #     self.assertEqual((organisation.name, organisation.email), ("Renamed", email))

    def test_update_does_not_create_a_second_organisation(self):
        before = Organisation.objects.count()

        self.service.update(self.request({"name": "Renamed"}, "PATCH"), 1)

        self.assertEqual(Organisation.objects.count(), before)

    def test_update_rejects_bad_input(self):
        _, http_status = self.service.update(self.request({"email": "nope"}, "PATCH"), 1)

        self.assertEqual(http_status, status.HTTP_400_BAD_REQUEST)

    def test_update_of_an_unknown_organisation(self):
        _, http_status = self.service.update(self.request({"name": "x"}, "PATCH"), 99999)

        self.assertEqual(http_status, status.HTTP_400_BAD_REQUEST)

    def test_delete_is_a_soft_delete(self):
        data, http_status = self.service.delete(self.request(), None)

        self.assertEqual((data, http_status), ({}, status.HTTP_204_NO_CONTENT))
        organisation = Organisation.objects.get(pk=1)
        self.assertTrue(organisation.is_deleted)
        self.assertEqual(organisation.change_user, self.user)

    def test_delete_of_an_unknown_or_deleted_organisation(self):
        self.service.location_id = 99999
        self.assertEqual(self.service.delete(self.request(), None)[1], status.HTTP_400_BAD_REQUEST)

        self.service.delete(self.request(), 1)
        self.assertEqual(self.service.delete(self.request(), 1)[1], status.HTTP_400_BAD_REQUEST)

    # ---------- list ----------
    def _list(self, **query):
        request = self.request(method="GET")
        request.query_params = query

        return list(self.service.get_list(request))

    def _make(self, name, **fields):
        return Organisation.objects.create(
            name=name,
            website=fields.pop("website", "https://example.org"),
            email=fields.pop("email", "info@example.org"),
            change_user=self.user,
            creation_user=self.user,
            **fields,
        )

    def test_list_has_every_organisation_that_is_not_deleted(self):
        self._make("Zed Ltd")
        deleted = self._make("Gone Ltd")
        Organisation.objects.filter(pk=deleted.pk).update(is_deleted=True)

        names = [organisation.name for organisation in self._list()]

        self.assertIn("Zed Ltd", names)
        self.assertNotIn("Gone Ltd", names)
        self.assertEqual(len(names), Organisation.objects.filter(is_deleted=False).count())

    def test_list_is_in_name_order(self):
        for name in ("Charlie", "Alpha", "Bravo"):  # same case: how upper and lower case sort depends on the database
            self._make(name)

        names = [organisation.name for organisation in self._list()]

        self.assertEqual(names, sorted(names))
        self.assertLess(names.index("Alpha"), names.index("Bravo"))
        self.assertLess(names.index("Bravo"), names.index("Charlie"))

    def test_list_can_be_searched_by_name_email_website_or_id(self):
        target = self._make("Searchable Pty", email="hello@searchable.example", website="https://searchable.example")
        self._make("Other Pty", email="other@other.example", website="https://other.example")

        for name, query in {
            "name": "searchable pty",
            "email": "HELLO@searchable",
            "website": "searchable.example",
            "id": str(target.pk),
        }.items():
            with self.subTest(name):
                self.assertEqual([organisation.pk for organisation in self._list(search=query)], [target.pk])

    def test_a_search_with_no_match_is_empty(self):
        self.assertEqual(self._list(search="no organisation is called this"), [])

    def test_an_empty_search_is_no_search(self):
        self.assertEqual(len(self._list(search="")), Organisation.objects.filter(is_deleted=False).count())

    def test_a_numeric_search_also_matches_names(self):
        target = self._make("Studio 54")

        self.assertIn(target.pk, [organisation.pk for organisation in self._list(search="54")])

    def test_deleted_organisations_are_not_found_by_search(self):
        target = self._make("Hidden Pty")
        Organisation.objects.filter(pk=target.pk).update(is_deleted=True)

        self.assertEqual(self._list(search="Hidden"), [])


class CustomerServiceTests(ServiceTestBase):
    service = CustomerService(destination="project", location_id=1)
    body = {"title": 1, "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.org"}

    def test_create(self):
        data, http_status = self.service.create(self.request(self.body))

        self.assertEqual(http_status, status.HTTP_201_CREATED)
        self.assertEqual((data["first_name"], data["last_name"], data["email"]), ("Ada", "Lovelace", "ada@example.org"))
        self.assertEqual(data["title"]["title"], "Mr")
        self.assertTrue(Customer.objects.filter(pk=data["id"], first_name="Ada").exists())

    def test_create_rejects_bad_input_and_saves_nothing(self):
        before = Customer.objects.count()

        for name, body in {
            "empty": {},
            "no first name": {**self.body, "first_name": ""},
            "bad email": {**self.body, "email": "nope"},
            "unknown title": {**self.body, "title": 999},
        }.items():
            with self.subTest(name):
                _, http_status = self.service.create(self.request(body))

                self.assertEqual(http_status, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Customer.objects.count(), before)

    # def test_update_changes_only_what_was_sent(self):
    #     customer = Customer.objects.get(pk=1)
    #     email = customer.email
    #
    #     data, http_status = self.service.update(self.request({"first_name": "Renamed"}, "PATCH"), 1)
    #
    #     self.assertEqual(http_status, status.HTTP_200_OK)
    #     self.assertEqual(data["first_name"], "Renamed")
    #     customer.refresh_from_db()
    #     self.assertEqual((customer.first_name, customer.email), ("Renamed", email))

    # def test_update_can_change_the_title(self):
    #     self.service.update(self.request({"title": 4}, "PATCH"), 1)
    #
    #     self.assertEqual(Customer.objects.get(pk=1).title_id, 4)

    # def test_update_does_not_create_a_second_customer(self):
    #     """update() used to call serializer.save() with no instance - it made a new customer every time"""
    #     before = Customer.objects.count()
    #
    #     self.service.update(self.request({"first_name": "Renamed"}, "PATCH"), 1)
    #
    #     self.assertEqual(Customer.objects.count(), before)

    # def test_update_rejects_bad_input_and_unknown_customers(self):
    #     self.assertEqual(self.service.update(self.request({"email": "nope"}, "PATCH"), 1)[1], status.HTTP_400_BAD_REQUEST)
    #     statuself.assertEqual(self.service.update(self.request({"first_name": "x"}, "PATCH"), 99999)[1], status.HTTP_400_BAD_REQUEST)

    def test_delete_is_a_soft_delete(self):
        data, http_status = self.service.delete(self.request(), 1)

        self.assertEqual((data, http_status), ({}, status.HTTP_204_NO_CONTENT))
        self.assertTrue(Customer.objects.get(pk=1).is_deleted)

    # def test_delete_of_an_unknown_or_deleted_customer(self):
    #     self.assertEqual(self.service.delete(self.request(), 99999)[1], status.HTTP_400_BAD_REQUEST)
    #
    #     self.service.delete(self.request(), 1)
    #     self.assertEqual(self.service.delete(self.request(), 1)[1], status.HTTP_400_BAD_REQUEST)

    # def test_get_list_gives_the_customers_linked_to_the_object(self):
    #     data, http_status = self.service.get_list(self.request())
    #
    #     self.assertEqual(http_status, status.HTTP_200_OK)
    #     linked = {customer["id"] for customer in data}
    #     self.assertTrue(linked.issubset({customer.pk for customer in Customer.objects.all()}))


class SprintServiceTests(ServiceTestBase):
    @staticmethod
    def service(pk=1):
        return SprintService(destination="sprint", location_id=pk)

    def test_retrieve(self):
        data, http_status = self.service(1).retrieve(self.request(method="GET"))

        self.assertEqual(http_status, status.HTTP_200_OK)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], Sprint.objects.get(pk=1).title)

    def test_retrieve_of_an_unknown_or_deleted_sprint_is_not_found(self):
        self.assertEqual(self.service(99999).retrieve(self.request())[1], status.HTTP_404_NOT_FOUND)

        Sprint.objects.filter(pk=1).update(is_deleted=True)
        self.assertEqual(self.service(1).retrieve(self.request())[1], status.HTTP_404_NOT_FOUND)

    def test_update_saves_the_change_and_who_made_it(self):
        data, http_status = self.service(1).update(self.request({"title": "Renamed sprint"}, "PATCH"), 1)

        self.assertEqual(http_status, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Renamed sprint")
        sprint = Sprint.objects.get(pk=1)
        self.assertEqual((sprint.title, sprint.change_user), ("Renamed sprint", self.user))

    def test_update_only_touches_one_sprint(self):
        others = list(Sprint.objects.exclude(pk=1).values_list("pk", "title"))

        self.service(1).update(self.request({"title": "Renamed sprint"}, "PATCH"), 1)

        self.assertEqual(list(Sprint.objects.exclude(pk=1).values_list("pk", "title")), others)

    def test_update_with_bad_input_is_a_400_not_a_status_of_false(self):
        """The error branch used to return False as the http status"""
        _, http_status = self.service(1).update(self.request({"start_date": "yesterday-ish"}, "PATCH"), 1)

        self.assertEqual(http_status, status.HTTP_400_BAD_REQUEST)

    def test_update_of_an_unknown_sprint_is_not_found(self):
        self.assertEqual(self.service(99999).update(self.request({"title": "x"}, "PATCH"), 99999)[1], status.HTTP_404_NOT_FOUND)

    def test_methods_that_are_not_built_yet_say_so(self):
        service = self.service()
        for call in (
            lambda: service.create(self.request()),
            lambda: service.delete(self.request(), 1),
            lambda: service.get_list(self.request()),
        ):
            with self.assertRaises(NotImplementedError):
                call()


class SprintObjectLinkServiceTests(ServiceTestBase):
    def test_nothing_is_built_yet(self):
        service = SprintObjectLinkService(destination="sprint", location_id=1)
        for call in (
            lambda: service.create(self.request()),
            lambda: service.delete(self.request(), 1),
            lambda: service.get_list(self.request()),
            lambda: service.update(self.request(), 1),
        ):
            with self.assertRaises(NotImplementedError):
                call()


class SprintLinkSerializerTests(ServiceTestBase):
    """This module could not even be imported (it took Requirement from the wrong place)"""

    def test_a_project_or_a_requirement_can_be_chosen(self):
        for body in ({"project": 1}, {"requirement": 1}, {}):
            with self.subTest(body=body):
                self.assertTrue(SprintLinkSerializer(data=body).is_valid())

    def test_unknown_and_deleted_objects_are_rejected(self):
        from NearBeach.models.project import Project

        Project.objects.filter(pk=2).update(is_deleted=True)

        for body in ({"project": 99999}, {"project": 2}, {"requirement": 99999}):
            with self.subTest(body=body):
                self.assertFalse(SprintLinkSerializer(data=body).is_valid())
