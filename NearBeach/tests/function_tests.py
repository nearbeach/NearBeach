from django.urls import reverse


def assertEqual200(response_array, self):
    # Look through the array to see if it response with 405
    for response in response_array:
        self.assertEqual(
            response.status_code,
            200
        )


def assertEqual405(response_array, self):
    # Look through the array to see if it response with 405
    for response in response_array:
        self.assertEqual(
            response.status_code,
            405
        )


def assertRedirectsToLogin(response_array, self):
    # Loop through the array to see if it redirects to login
    for response in response_array:
        self.assertRedirects(
            response,
            reverse('login'),
            status_code=302,
            target_status_code=200,
            msg_prefix='',
            fetch_redirect_response=True
        )
