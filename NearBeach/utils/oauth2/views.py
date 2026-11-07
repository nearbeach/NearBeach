from django.http import JsonResponse
from oauth2_provider.views import TokenView

from NearBeach.utils.throttle.AuthHourThrottle import AuthHourThrottle
from NearBeach.utils.throttle.AuthMinuteThrottle import AuthMinuteThrottle


class ThrottledTokenView(TokenView):
    """The token endpoint, held to the same rate limits as the login endpoint to slow down credential guessing"""

    def dispatch(self, request, *args, **kwargs):
        for throttle in (AuthMinuteThrottle(), AuthHourThrottle()):
            if not throttle.allow_request(request, self):
                return JsonResponse({"error": "too_many_requests"}, status=429)

        return super().dispatch(request, *args, **kwargs)
