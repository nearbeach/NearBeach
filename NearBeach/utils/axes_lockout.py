from django.http import HttpRequest, HttpResponse, JsonResponse

from NearBeach.utils.enums.login_status_enum import LoginStatusEnum


def lockout_response(
    request: HttpRequest,
    response: HttpResponse | None = None,
    credentials: dict | None = None,
) -> JsonResponse:
    """Replaces django-axes' default lockout page with the JSON the login screen understands.

    The body is identical whether or not the username exists, so the lockout can't be used to
    discover valid accounts.
    """
    return JsonResponse(
        {"status": LoginStatusEnum.LOCKED_OUT},
        status=429,
    )
