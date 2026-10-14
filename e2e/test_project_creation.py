import re
from uuid import uuid4

import pytest
from playwright.sync_api import Page, expect


def test_create_project(authenticated_page: Page, app_url, e2e_group):
    page = authenticated_page
    project_title = f"QA project {uuid4().hex[:10]}"

    page.goto(f"{app_url}/project/new")
    page.get_by_placeholder("Your project's title", exact=True).fill(project_title)

    group_select = page.locator('select[name="Select Group"]')
    group_select.select_option(label=e2e_group.name, timeout=10_000)
    expect(group_select.locator("option:checked")).to_have_text(e2e_group.name)

    create_button = page.get_by_role("button", name="Create", exact=True)
    with page.expect_response(
        lambda response: (
            response.request.method == "POST"
            and response.url == f"{app_url}/api/v1/project/"
        )
    ) as response_info:
        create_button.click()

    response = response_info.value
    if response.status != 201:
        pytest.fail(
            f"Project creation failed: {response.status}\n{response.text()}"
        )
    expect(page).to_have_url(re.compile(rf"^{re.escape(app_url)}/project/\d+/?$"))

    title_input = page.get_by_placeholder("Your project title", exact=True)
    expect(title_input).to_have_value(project_title)
    page.reload()
    expect(title_input).to_have_value(project_title)
    expect(
        page.locator(".group-access-list").get_by_text(e2e_group.name, exact=True)
    ).to_be_visible()
