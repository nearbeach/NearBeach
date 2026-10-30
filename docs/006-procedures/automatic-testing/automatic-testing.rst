Automatic Testing
#################

NearBeach has the following automatic testing setup;

- Backend Unit Tests
- Frontend Unit Tests
- Frontend End-to-end tests
- Backend API Fuzzy Testing
- Database Index Benchmarking


Backend Unit Testing
====================

Activate your python virtual environment

    source ./venv/bin/activate

Make sure you have installed all dev requirements

    pip install -r requirements-dev.txt
    pip install -r requirements-e2e.txt

Run the tests

    python3 ./manage.py test

Good luck - it will take time


Frontend Unit Tests
===================

Make sure you have all the node libraries

    npm install

Run the following command

    npm run test:unit


Frontend End-to-end tests
=========================

Make sure you have all the node libraries

    npm install

Run the following command

    npm run test:e2e


Backend API Fuzzy Testing
=========================

Activate your python virtual environment

    source ./venv/bin/activate

Make sure you have installed all dev requirements

    pip install -r requirements-dev.txt
    pip install -r requirements-e2e.txt

Run the tests as either admin, or run as a restricted user

    scripts/run_schemathesis.sh admin
    scripts/run_schemathesis.sh read_only


What the script does
--------------------

1. It creates a throw-away sqlite DB in a temp dir, using local/settings_schemathesis.py. It refuses to run if the DB
   path would be db.sqlite3, so your real data is safe.

2. It runs migrate, loads the NearBeach_basic_setup.json fixture, and generates the OpenAPI schema with spectacular.

3. It starts runserver on port 8765, with throttling turned off.

4. It runs schemathesis run against it. The authentication endpoints are excluded.

5. It cleans up the server and the temp DB when it finishes.


Useful knobs (env vars)
-----------------------

Also check schema and status-code conformance, not just "no 500s"

    SCHEMATHESIS_CHECKS=all scripts/run_schemathesis.sh admin

Fuzz harder (default is 50)
    SCHEMATHESIS_MAX_EXAMPLES=500 scripts/run_schemathesis.sh admin

Try a different random seed (default is 1)
    SCHEMATHESIS_SEED=42 scripts/run_schemathesis.sh admin

Pass extra schemathesis args after --
    scripts/run_schemathesis.sh admin -- --include-path-regex '^/api/v1/projects/'

Other variables are SCHEMATHESIS_PASSWORD (default Test1234$), SCHEMATHESIS_PORT and PYTHON.


Database Index Benchmarking
===========================

scripts/benchmark_indexes.py seeds a throw-away database with a large number of rows, then times NearBeach's list and
search queries before and after adding candidate indexes. Use it to check that an index (or a query rewrite) really
helps before it goes into a migration, and to re-check the existing indexes after large model or query changes.

It never touches your real database. SQLite writes to benchmark.sqlite3 in the repo root, and the MySQL and
PostgreSQL options use a separate empty database. The queries in the script are copies of the real ones in
ProjectService, OrganisationService and the potential object links view - if those change, update the script too.

Activate your python virtual environment

    source ./venv/bin/activate


Run against SQLite (quickest)
-----------------------------

    python scripts/benchmark_indexes.py --rows 1000000 --explain

1,000,000 rows takes about 5 minutes to seed. Delete benchmark.sqlite3 when you are finished, or point it elsewhere
with BENCH_DB=/path/to/file.sqlite3.


Run against MySQL (matches production)
--------------------------------------

Production runs MySQL, so this is the run to trust. You need

- a MySQL 8 (or newer) server, for example in Docker
- an empty database, and a user with all privileges on it
- the mysqlclient python package (pymysql also works if mysqlclient is not installed)

Create the database

    CREATE DATABASE nearbeach_bench CHARACTER SET utf8mb4;

Run the benchmark

    BENCH_ENGINE=mysql BENCH_MYSQL_USER=nearbeach_benchmark python scripts/benchmark_indexes.py --rows 1000000 --explain

Other variables are BENCH_MYSQL_NAME (default nearbeach_bench), BENCH_MYSQL_PASSWORD, BENCH_MYSQL_HOST (default
127.0.0.1) and BENCH_MYSQL_PORT (default 3306).

Seeding 1,000,000 rows takes about 7 minutes on MySQL. The script migrates and seeds the database it is pointed at, so
drop and recreate the database before a fresh run

    DROP DATABASE nearbeach_bench; CREATE DATABASE nearbeach_bench CHARACTER SET utf8mb4;


Run against PostgreSQL
----------------------

This is supported but has not been tested. Set BENCH_ENGINE=postgres together with BENCH_PG_NAME, BENCH_PG_USER,
BENCH_PG_PASSWORD, BENCH_PG_HOST and BENCH_PG_PORT. The pg_trgm extension is used for the text search candidates.


Useful options
--------------

Smaller, faster run while changing the script

    python scripts/benchmark_indexes.py --rows 200000

Re-use an already seeded database (it is not re-seeded, so the row count is whatever it was seeded with)

    python scripts/benchmark_indexes.py --skip-seed

More timed runs per query for steadier numbers (default is 3, the median is reported)

    python scripts/benchmark_indexes.py --skip-seed --runs 5


Reading the results
-------------------

1. BASELINE is timed with no candidate indexes, then the candidate indexes are created, then WITH INDEXES is timed.

2. The SUMMARY table at the end shows the median time in milliseconds before and after, and the speedup. Anything
   under 1.0x got slower - do not add that index.

3. Rows starting with ALT are alternative ways of writing a query (for example an EXISTS rewrite, istartswith, or a
   MySQL FULLTEXT search) compared against the current one. n/a in the before column means the case needs an index
   that does not exist yet.

4. --explain prints the database's query plan for each query before and after, which shows why a result moved.

5. Trust the ratios more than the absolute times. Timings depend heavily on hardware, the database's memory settings
   (the default MySQL Docker buffer pool is only 128 MB) and what else is running, so expect noise of 20-30%.

6. The seeded data is synthetic. The test user sees about 10% of all objects through 5 of 50 groups, so a user in
   every group will be slower than the numbers shown.


Candidate indexes
-----------------

The candidate indexes are listed in candidate_indexes() in the script. They are created with raw SQL so the script
never creates migrations. When an index proves worthwhile, add it as models.Index in the model's Meta class and
create a normal migration (see migration 0053 for an example). MySQL has no partial indexes, so the script drops the
WHERE clause on MySQL. MySQL also drops Django's own foreign key index when a composite index starts with the same
column, so the script restores a plain index between runs to keep the baseline honest.
