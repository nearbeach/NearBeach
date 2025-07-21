from django.urls import reverse


def assert_equal200(response_array, self):
    # Look through the array to see if it response with 200
    for response in response_array:
        self.assertEqual(response.status_code, 200)


def assert_equal405(response_array, self):
    # Look through the array to see if it response with 405
    for response in response_array:
        self.assertEqual(response.status_code, 405)


def assert_redirects_to_login(response_array, self):
    # Loop through the array to see if it redirects to login
    for response in response_array:
        self.assertRedirects(
            response,
            reverse("login"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
