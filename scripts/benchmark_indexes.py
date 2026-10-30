"""
Seed a throwaway database with lots of rows, then time NearBeach's search/list queries before and after
adding candidate indexes. Nothing here touches the real dev database or the migrations.

    venv/bin/python scripts/benchmark_indexes.py --rows 1000000
    venv/bin/python scripts/benchmark_indexes.py --rows 1000000 --skip-seed      # reuse seeded db

SQLite is the default (benchmark.sqlite3, git-ignored by being untracked - delete it when done).
For PostgreSQL set BENCH_ENGINE=postgres and BENCH_PG_NAME/USER/PASSWORD/HOST/PORT.
"""

import argparse
import os
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scripts.benchmark_settings")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.management import call_command  # noqa: E402
from django.db import DatabaseError, connection  # noqa: E402
from django.db.models import Exists, OuterRef, Q  # noqa: E402

from NearBeach.models.object_assignment.object_assignment import ObjectAssignment  # noqa: E402
from NearBeach.models.organisation import Organisation  # noqa: E402
from NearBeach.models.permission.group import Group  # noqa: E402
from NearBeach.models.permission.permission_set import PermissionSet  # noqa: E402
from NearBeach.models.project import ListOfProjectStatus, Project  # noqa: E402
from NearBeach.models.task import ListOfTaskStatus, Task  # noqa: E402
from NearBeach.models.user import UserGroup  # noqa: E402

BATCH = 5000
WORDS = (
    "alpha beta gamma delta website migration invoice customer onboarding report budget review sprint "
    "release security audit mobile redesign payment support upgrade integration roadmap training data"
).split()
IS_POSTGRES = connection.vendor == "postgresql"
IS_MYSQL = connection.vendor == "mysql"


def _title(rng: random.Random) -> str:
    return " ".join(rng.choices(WORDS, k=4)) + f" {rng.randint(1, 99999)}"


def _bulk(model, objs):
    model.objects.bulk_create(objs, batch_size=BATCH)


def seed(rows: int) -> None:
    rng = random.Random(42)
    started = time.time()
    call_command("migrate", verbosity=0, interactive=False)

    User = get_user_model()
    if User.objects.exists():
        print("Database already seeded - use --skip-seed or delete the benchmark db")
        return
    user = User.objects.create_user("bench", "bench@example.com", "bench")
    User.objects.create_user("other", "other@example.com", "other")
    permission_set = PermissionSet.objects.create(name="bench", change_user=user, creation_user=user)
    groups = [Group(name=f"group {i}", change_user=user, creation_user=user) for i in range(50)]
    _bulk(Group, groups)
    group_ids = list(Group.objects.values_list("id", flat=True))
    # The bench user is in 5 of 50 groups -> sees roughly 10% of all objects
    for group_id in group_ids[:5]:
        UserGroup.objects.create(
            username=user, group_id=group_id, permission_set=permission_set, change_user=user, creation_user=user
        )
    # Other users, so UserGroup isn't tiny
    for group_id in group_ids:
        UserGroup.objects.create(
            username_id=2, group_id=group_id, permission_set=permission_set, change_user=user, creation_user=user
        )

    project_status = [
        ListOfProjectStatus.objects.create(status=s, higher_order_status=h, change_user=user, creation_user=user)
        for s, h in (("New", "Normal"), ("In Progress", "Normal"), ("Closed", "Closed"))
    ]
    task_status = [
        ListOfTaskStatus.objects.create(status=s, higher_order_status=h, change_user=user, creation_user=user)
        for s, h in (("New", "Normal"), ("In Progress", "Normal"), ("Closed", "Closed"))
    ]

    def seed_table(label, count, make):
        done = 0
        while done < count:
            n = min(BATCH * 10, count - done)
            _bulk(make[0], [make[1](done + i) for i in range(n)])
            done += n
            print(f"  {label}: {done:,}/{count:,}", end="\r")
        print()

    print(f"Seeding {rows:,} projects, {rows:,} tasks, {rows // 5:,} organisations ...")
    seed_table(
        "organisations",
        rows // 5,
        (
            Organisation,
            lambda i: Organisation(
                name=f"{rng.choice(WORDS).title()} {rng.choice(WORDS).title()} {i}",
                website=f"www.{rng.choice(WORDS)}{i}.com",
                email=f"info{i}@{rng.choice(WORDS)}.com",
                is_deleted=rng.random() < 0.05,
            ),
        ),
    )
    seed_table(
        "projects",
        rows,
        (
            Project,
            lambda i: Project(
                title=_title(rng),
                status=rng.choice(project_status),
                is_deleted=rng.random() < 0.05,
            ),
        ),
    )
    seed_table(
        "tasks",
        rows,
        (
            Task,
            lambda i: Task(
                title=_title(rng),
                status=rng.choice(task_status),
                is_deleted=rng.random() < 0.05,
            ),
        ),
    )
    # One group assignment per project / task (ids are 1..N on a fresh database)
    seed_table(
        "project assignments",
        rows,
        (
            ObjectAssignment,
            lambda i: ObjectAssignment(project_id=i + 1, group_id=rng.choice(group_ids)),
        ),
    )
    seed_table(
        "task assignments",
        rows,
        (
            ObjectAssignment,
            lambda i: ObjectAssignment(task_id=i + 1, group_id=rng.choice(group_ids)),
        ),
    )
    print(f"Seeded in {time.time() - started:.0f}s")


# ---------------------------------------------------------------------------------------------------------------
# Queries - copied from the real services/views so we measure what production runs
# ---------------------------------------------------------------------------------------------------------------
def _user_groups(user):
    return UserGroup.objects.filter(is_deleted=False, username=user).values("group_id")


def project_list(user, search=None):
    assignments = ObjectAssignment.objects.filter(
        project_id__isnull=False, is_deleted=False, group_id__in=_user_groups(user)
    )
    results = Project.objects.filter(is_deleted=False, id__in=assignments.values("project_id"))
    if search:
        results = results.filter(Q(title__icontains=search) | Q(id=int(search) if search.isdigit() else None))
    return results.exclude(status__higher_order_status="Closed")


def project_list_exists(user, search=None):
    """Same result as project_list, but a correlated EXISTS so the database can walk projects by id and stop early"""
    assignment = ObjectAssignment.objects.filter(
        project_id=OuterRef("pk"), is_deleted=False, group_id__in=_user_groups(user)
    )
    results = Project.objects.filter(Exists(assignment), is_deleted=False)
    if search:
        results = results.filter(Q(title__icontains=search) | Q(id=int(search) if search.isdigit() else None))
    return results.exclude(status__higher_order_status="Closed")


def organisation_list(search):
    return Organisation.objects.filter(is_deleted=False).order_by("name", "pk").filter(
        Q(name__icontains=search)
        | Q(email__icontains=search)
        | Q(website__icontains=search)
        | Q(id=int(search) if search.isdigit() else None)
    )


def potential_links_tasks(user):
    assignments = ObjectAssignment.objects.filter(is_deleted=False, group_id__in=_user_groups(user))
    return Task.objects.filter(
        is_deleted=False, id__in=assignments.filter(task_id__isnull=False).values("task_id")
    ).values("id", "title")


def build_cases(user):
    """(label, callable returning a queryset, how to execute it)"""
    cases = [
        ("project list, no search - page 1 (count + 25 rows)", lambda: project_list(user), "page"),
        ("project list, search 'invoice' - page 1", lambda: project_list(user, "invoice"), "page"),
        ("project list, search by id", lambda: project_list(user, "424242"), "page"),
        ("organisation list, search 'budget' - page 1", lambda: organisation_list("budget"), "page"),
        ("potential links (tasks), unbounded as today", lambda: potential_links_tasks(user), "all"),
    ]
    cases += [
        ("ALT project list, EXISTS rewrite - page 1 (count + 25)", lambda: project_list_exists(user), "page"),
        ("ALT project list, current query - 25 rows only (no count)", lambda: project_list(user), "rows"),
        ("ALT project list, EXISTS rewrite - 25 rows only (no count)", lambda: project_list_exists(user), "rows"),
        ("ALT project list, EXISTS - search 'invoice' page 1", lambda: project_list_exists(user, "invoice"), "page"),
    ]
    if IS_MYSQL:
        # Alternatives to icontains: MySQL FULLTEXT (ngram) and prefix matching
        cases += [
            (
                "ALT project search 'invoice' via FULLTEXT MATCH",
                lambda: project_list(user).extra(
                    where=["MATCH(title) AGAINST (%s IN BOOLEAN MODE)"], params=["invoice"]
                ),
                "page",
            ),
            (
                "ALT project search 'invoice' via istartswith",
                lambda: project_list(user).filter(title__istartswith="invoice"),
                "page",
            ),
        ]
    return cases


def run_case(factory, mode):
    queryset = factory()
    if mode == "page":
        queryset.count()
        list(queryset[:25])
    elif mode == "rows":
        list(queryset[:25])
    else:
        list(queryset)


def bench(user, runs):
    results = {}
    for label, factory, mode in build_cases(user):
        times = []
        try:
            for _ in range(runs):
                t0 = time.perf_counter()
                run_case(factory, mode)
                times.append(time.perf_counter() - t0)
        except DatabaseError as exc:  # e.g. FULLTEXT MATCH before its index exists
            results[label] = None
            print(f"  {'n/a':>10}     {label}  ({exc.args[-1] if exc.args else exc})")
            continue
        results[label] = statistics.median(times)
        print(f"  {results[label] * 1000:10.1f} ms  {label}")
    return results


# ---------------------------------------------------------------------------------------------------------------
# Candidate indexes (raw SQL so the benchmark never creates migrations)
# ---------------------------------------------------------------------------------------------------------------
def candidate_indexes():
    oa, ug = ObjectAssignment._meta.db_table, UserGroup._meta.db_table
    pr, tk, og = Project._meta.db_table, Task._meta.db_table, Organisation._meta.db_table
    # MySQL has no partial indexes, so the WHERE clause is only used on SQLite / PostgreSQL
    not_null = lambda column: "" if IS_MYSQL else f" WHERE {column} IS NOT NULL"  # noqa: E731
    indexes = [
        ("bench_ug_user_deleted_group", f"{ug} (username_id, is_deleted, group_id)"),
        ("bench_oa_group_project", f"{oa} (group_id, is_deleted, project_id){not_null('project_id')}"),
        ("bench_oa_group_task", f"{oa} (group_id, is_deleted, task_id){not_null('task_id')}"),
        ("bench_project_deleted_status", f"{pr} (is_deleted, status_id)"),
        ("bench_task_deleted_status", f"{tk} (is_deleted, status_id)"),
        ("bench_org_deleted_name", f"{og} (is_deleted, name)"),
    ]
    if IS_MYSQL:
        indexes += [
            ("bench_project_title_ft", f"{pr} (title) WITH PARSER ngram"),
            ("bench_org_name_ft", f"{og} (name) WITH PARSER ngram"),
            ("bench_project_title_prefix", f"{pr} (is_deleted, title(40))"),
        ]
    if IS_POSTGRES:
        indexes += [
            ("bench_project_title_trgm", f"{pr} USING gin (upper(title) gin_trgm_ops)"),
            ("bench_org_name_trgm", f"{og} USING gin (upper(name) gin_trgm_ops)"),
        ]
    return indexes


def apply_indexes(create: bool):
    with connection.cursor() as cursor:
        if IS_POSTGRES and create:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        for name, definition in candidate_indexes():
            if IS_MYSQL:
                table = definition.split(" ", 1)[0]
                cursor.execute(f"SHOW INDEX FROM {table} WHERE Key_name = %s", [name])
                if cursor.fetchall():
                    try:
                        cursor.execute(f"DROP INDEX {name} ON {table}")
                    except DatabaseError:
                        # MySQL dropped the original foreign key index when our composite one covered it, so
                        # restore a plain index on the leading column (Django's default state) and retry
                        lead = definition.split("(", 1)[1].split(",")[0].split(")")[0].strip()
                        cursor.execute(f"CREATE INDEX fk_{name} ON {table} ({lead})")
                        cursor.execute(f"DROP INDEX {name} ON {table}")
            else:
                cursor.execute(f"DROP INDEX IF EXISTS {name}")
            if create:
                t0 = time.time()
                kind = "FULLTEXT INDEX" if definition.endswith("WITH PARSER ngram") else "INDEX"
                cursor.execute(f"CREATE {kind} {name} ON {definition}")
                print(f"  created {name} in {time.time() - t0:.1f}s")
        if IS_MYSQL:
            for table in {d.split(" ", 1)[0] for _, d in candidate_indexes()}:
                cursor.execute(f"ANALYZE TABLE {table}")
                cursor.fetchall()
        else:
            cursor.execute("ANALYZE")


def explain(user):
    for label, factory, mode in build_cases(user):
        print(f"\n--- {label}")
        try:
            print(factory().explain())
        except Exception as exc:  # noqa: BLE001 - report and carry on
            print(f"(explain failed: {exc})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1_000_000, help="rows per big table (projects, tasks)")
    parser.add_argument("--runs", type=int, default=3, help="timed runs per query (median reported)")
    parser.add_argument("--skip-seed", action="store_true")
    parser.add_argument("--explain", action="store_true", help="also print query plans before/after")
    args = parser.parse_args()

    print(f"Database: {connection.vendor} -> {connection.settings_dict['NAME']}")
    if not args.skip_seed:
        seed(args.rows)

    user = get_user_model().objects.get(username="bench")
    apply_indexes(create=False)
    print("\nBASELINE (no candidate indexes)")
    before = bench(user, args.runs)
    if args.explain:
        explain(user)

    print("\nCreating candidate indexes")
    apply_indexes(create=True)
    print("\nWITH INDEXES")
    after = bench(user, args.runs)
    if args.explain:
        explain(user)

    print("\nSUMMARY (median ms)")
    print(f"{'query':58} {'before':>10} {'after':>10} {'speedup':>8}")
    for label in before:
        b, a = before[label], after[label]
        b_text = f"{b * 1000:10.1f}" if b is not None else f"{'n/a':>10}"
        a_text = f"{a * 1000:10.1f}" if a is not None else f"{'n/a':>10}"
        speedup = f"{b / a:7.1f}x" if b and a else f"{'':>8}"
        print(f"{label:58} {b_text} {a_text} {speedup}")


if __name__ == "__main__":
    main()
