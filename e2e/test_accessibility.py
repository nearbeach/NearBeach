"""Automated accessibility (axe-core) checks against the main pages.

Violations are grouped by rule. Known issues from A11Y_REPORT.md are listed
in KNOWN_ISSUES and marked xfail (strict) so they are visible, and so the test
starts failing as soon as one is fixed and should be removed from the list.
"""

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page, expect

from NearBeach.models.object_assignment.object_assignment import ObjectAssignment
from NearBeach.models.project import ListOfProjectStatus, Project

WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]

# page key -> axe rule ids already reported in A11Y_REPORT.md
# (form labels from the wlk form library fail AA contrast - found by this suite)
_FORM = {"color-contrast"}
KNOWN_ISSUES: dict[str, set[str]] = {
    "/project/new": _FORM,
    # A11Y_REPORT #3: unlabelled relationship select and icon-only add button
    "/project/<id>#Linked Objects": _FORM | {"select-name", "button-name"},
    "/project/<id>#Documentation": _FORM,
    "/project/<id>#Notes": _FORM,
    "/project/<id>#Misc": _FORM,
}


@pytest.fixture
def project(e2e_user, e2e_group, authenticated_session):
    audit_fields = {"creation_user": e2e_user, "change_user": e2e_user}
    project = Project.objects.create(
        title="A11Y project",
        status=ListOfProjectStatus.objects.filter(is_deleted=False).first(),
        **audit_fields,
    )
    ObjectAssignment.objects.create(
        project=project, group=e2e_group, **audit_fields
    )
    return project


def _run_axe(page: Page):
    return Axe().run(page, options={"runOnly": {"type": "tag", "values": WCAG_TAGS}})


def _format(violations) -> str:
    lines = []
    for violation in violations:
        lines.append(
            f"[{violation['impact']}] {violation['id']}: {violation['help']} "
            f"({len(violation['nodes'])} nodes)"
        )
        for node in violation["nodes"][:3]:
            lines.append(f"    {node['target']}")
    return "\n".join(lines)


def _assert_no_new_violations(page: Page, key: str):
    results = _run_axe(page)
    violations = results.response["violations"]
    known = KNOWN_ISSUES.get(key, set())
    new = [v for v in violations if v["id"] not in known]
    assert not new, f"{key}: new a11y violations\n{_format(new)}"
    still_present = {v["id"] for v in violations}
    fixed = known - still_present
    assert not fixed, f"{key}: fixed, remove from KNOWN_ISSUES: {sorted(fixed)}"


def _wait_for_app(page: Page):
    page.wait_for_load_state("networkidle")
    expect(page.locator("main, #app").first).to_be_visible()


@pytest.mark.parametrize(
    "path",
    ["/", "/project/new", "/project"],
    ids=["dashboard", "project-new", "project-search"],
)
def test_page_has_no_axe_violations(authenticated_page: Page, app_url, path):
    authenticated_page.goto(f"{app_url}{path}")
    _wait_for_app(authenticated_page)
    _assert_no_new_violations(authenticated_page, path)


@pytest.mark.parametrize("tab", ["Linked Objects", "Documentation", "Notes", "Misc"])
def test_project_details_tabs_have_no_axe_violations(
    authenticated_page: Page, app_url, project, tab
):
    page = authenticated_page
    page.goto(f"{app_url}/project/{project.pk}")
    _wait_for_app(page)
    # Linked Objects renders asynchronously; scan only once it is present
    page.locator("#relationship-type").wait_for(state="attached")
    page.get_by_role("tab", name=tab).click()
    _assert_no_new_violations(page, f"/project/<id>#{tab}")


@pytest.mark.xfail(strict=True, reason="A11Y_REPORT #7: every page is 'NearBeach Application'")
def test_page_titles_are_descriptive(authenticated_page: Page, app_url):
    """WCAG 2.4.2 - report notes every page is titled 'NearBeach Application'."""
    page = authenticated_page
    titles = set()
    for path in ("/project/new", "/project"):
        page.goto(f"{app_url}{path}")
        _wait_for_app(page)
        titles.add(page.title())
    assert len(titles) == 2, f"pages share a generic title: {titles}"


@pytest.mark.xfail(strict=True, reason="A11Y_REPORT #2: menu toggle is a div, not a button")
def test_header_navigation_reachable_by_keyboard_on_mobile(
    authenticated_page: Page, app_url
):
    """WCAG 2.1.1 - the mobile menu toggle must be focusable and named."""
    page = authenticated_page
    page.set_viewport_size({"width": 375, "height": 812})
    page.goto(f"{app_url}/project")
    _wait_for_app(page)
    toggle = page.locator("header").get_by_role("button").first
    expect(toggle).to_be_visible()
    toggle.focus()
    expect(toggle).to_be_focused()
    expect(toggle).to_have_attribute("aria-expanded", "false")
