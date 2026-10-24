"""The API documentation has to describe what the API really sends.

Each case was a response/schema mismatch found by Schemathesis (scripts/run_schemathesis.sh).
The first half checks the real responses, the second half checks the generated OpenAPI schema.
"""
from drf_spectacular.generators import SchemaGenerator

from NearBeach.tests.utils.BaseApiClass import BaseApiClass


class ResponseShapeTests(BaseApiClass):
    username = "admin"
    password = "Test1234$"

    def test_project_user_list_has_full_names(self):
        users = self.client.get("/api/v1/project/1/").data["user_list"]

        self.assertGreater(len(users), 0)
        for user in users:
            with self.subTest(user=user["username"]):
                self.assertEqual(user["full_name"], f'{user["first_name"]} {user["last_name"]}')

    def test_group_and_user_ids_are_integers(self):
        data = self.client.get("/api/v1/project/1/groups/").data

        for group in data["group_list"]:
            self.assertIsInstance(group["id"], int)
        for user in data["user_list"] + data["potential_user_list"]:
            self.assertIsInstance(user["id"], int)
            self.assertIn("full_name", user)

    def test_potential_object_links_only_send_identifying_fields(self):
        links = self.client.get("/api/v1/data/potential_object_links/").data

        self.assertGreater(len(links), 0)
        for link in links:
            self.assertEqual(set(link), {"object_id", "object_title", "object_type"})

    def test_project_without_an_organisation_serializes_organisation_as_null(self):
        created = self.client.post(
            "/api/v1/project/", {"title": "No organisation", "group_list": [1]}, format="json"
        )

        self.assertEqual(created.status_code, 201)
        self.assertIsNone(created.data["organisation"])

    def test_customer_create_returns_the_customer_list(self):
        response = self.client.post("/api/v1/project/1/customer/", {"id": 1}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(response.data, list)

    def test_priority_is_sent_as_value_and_label(self):
        priority = self.client.get("/api/v1/project/1/").data["priority"]

        self.assertEqual(set(priority), {"value", "label"})

    def test_patch_sends_back_the_documented_fields_only(self):
        response = self.client.patch("/api/v1/project/1/", {"title": "New title"}, format="json")

        self.assertEqual(response.status_code, 200)
        for field in ("organisation", "group_list", "user_list"):
            self.assertNotIn(field, response.data)


class GeneratedSchemaTests(BaseApiClass):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.schema = SchemaGenerator().get_schema(request=None, public=True)
        cls.components = cls.schema["components"]["schemas"]

    def test_ids_are_documented_as_integers(self):
        for name in ("Group", "ParentGroup", "Customer", "Organisation"):
            with self.subTest(name):
                self.assertEqual(self.components[name]["properties"]["id"]["type"], "integer")

    def test_user_always_has_a_full_name(self):
        user = self.components["User"]

        self.assertEqual(user["properties"]["full_name"]["type"], "string")
        self.assertIn("full_name", user["required"])

    def test_patch_is_documented_with_its_own_shape(self):
        patch = self.schema["paths"]["/api/v1/project/{id}/"]["patch"]
        response = patch["responses"]["200"]["content"]["application/json"]["schema"]
        self.assertEqual(response, {"$ref": "#/components/schemas/ProjectPatch"})

        project_patch = self.components["ProjectPatch"]
        for field in ("organisation", "group_list", "user_list"):
            self.assertNotIn(field, project_patch["properties"])
            self.assertNotIn(field, project_patch.get("required", []))

    def test_project_user_list_is_not_required(self):
        """user_list is added by retrieve only - list and create responses do not have it"""
        self.assertNotIn("user_list", self.components["Project"].get("required", []))

    def test_project_organisation_can_be_null(self):
        self.assertTrue(self.components["Project"]["properties"]["organisation"].get("nullable"))

    def test_potential_object_links_are_documented_without_relationship_fields(self):
        link = self.components["PotentialObjectLink"]

        self.assertEqual(set(link["required"]), {"object_id", "object_title", "object_type"})
        self.assertNotIn("link_relationship", link["properties"])

    def test_pictures_can_be_null(self):
        for name in ("User", "Customer", "Organisation"):
            with self.subTest(name):
                self.assertTrue(self.components[name]["properties"]["profile_picture_path"].get("nullable"))

        self.assertTrue(self.components["User"]["properties"]["profile_picture"].get("nullable"))
        self.assertTrue(self.components["Note"]["properties"]["profile_picture"].get("nullable"))

    def test_priority_is_documented_as_value_and_label(self):
        priority = self.components["ProjectPatch"]["properties"]["priority"]

        self.assertEqual(priority["type"], "object")
        self.assertEqual(set(priority["properties"]), {"value", "label"})

    def test_retrieve_is_documented_with_readable_groups_and_users(self):
        get = self.schema["paths"]["/api/v1/project/{id}/"]["get"]
        response = get["responses"]["200"]["content"]["application/json"]["schema"]
        self.assertEqual(response, {"$ref": "#/components/schemas/ProjectDetail"})

        detail = self.components["ProjectDetail"]["properties"]
        self.assertEqual(detail["group_list"]["type"], "array")
        self.assertIn("user_list", detail)

    def test_customer_create_is_documented_as_the_list_it_returns(self):
        post = self.schema["paths"]["/api/v1/project/{id}/customer/"]["post"]
        response = post["responses"]["201"]["content"]["application/json"]["schema"]

        self.assertEqual(response["type"], "array")
