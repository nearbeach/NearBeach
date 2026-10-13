import pytest
from django.conf import settings
from django.middleware.csrf import get_token
from django.test import Client, RequestFactory
from playwright.sync_api import Page

from NearBeach.models import Group, ListOfProjectStatus, PermissionSet, UserGroup
from NearBeach.utils.enums.permission_enums import PermissionLevel


@pytest.fixture
def app_url(live_server):
    return live_server.url


@pytest.fixture
def e2e_user(transactional_db, django_user_model):
    return django_user_model.objects.create_user(
        username="qa_e2e",
        password=None,
    )


@pytest.fixture
def e2e_group(e2e_user):
    return Group.objects.create(
        name="E2E project team",
        creation_user=e2e_user,
        change_user=e2e_user,
    )


@pytest.fixture
def authenticated_session(e2e_user, e2e_group):
    audit_fields = {"creation_user": e2e_user, "change_user": e2e_user}

    # Transactional cleanup can remove migration-created statuses.
    if not ListOfProjectStatus.objects.filter(is_deleted=False).exists():
        ListOfProjectStatus.objects.create(
            status="New",
            sort_order=0,
            **audit_fields,
        )

    permissions = PermissionSet.objects.create(
        name="E2E project creator",
        project=PermissionLevel.ADD_AND_EDIT,
        **audit_fields,
    )
    UserGroup.objects.create(
        username=e2e_user,
        group=e2e_group,
        permission_set=permissions,
        **audit_fields,
    )

    client = Client()
    client.force_login(e2e_user)
    return client.cookies[settings.SESSION_COOKIE_NAME].value


@pytest.fixture
def authenticated_page(authenticated_session, app_url, page: Page) -> Page:
    csrf_request = RequestFactory().get("/")
    get_token(csrf_request)

    page.context.add_cookies(
        [
            {
                "name": settings.SESSION_COOKIE_NAME,
                "value": authenticated_session,
                "url": app_url,
                "httpOnly": True,
                "sameSite": "Lax",
            },
            {
                "name": settings.CSRF_COOKIE_NAME,
                "value": csrf_request.META["CSRF_COOKIE"],
                "url": app_url,
                "httpOnly": False,
                "sameSite": "Lax",
            },
        ]
    )
    return page
