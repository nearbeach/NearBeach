Automatic Testing
#################

NearBeach has the following automatic testing setup;

- Backend Unit Tests
- Frontend Unit Tests
- Frontend End-to-end tests
- Backend API Fuzzy Testing
- API Request Profiling (Silk)


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


API Request Profiling (Silk)
============================

NearBeach's frontend talks to the backend entirely through API calls, so tools that only decorate HTML pages (such as
Django Debug Toolbar) cannot show what an API call did. Django Silk records every request on the server, including JSON
API calls, with the SQL queries it ran and a Python profile of where the time went. Use it to find slow endpoints and
N+1 queries (the same query repeated once per row) while you develop.

Silk is for local development only. It is configured in local/settings.py and is not part of any production setup. It
writes every request to the database and slows requests down, so never enable it on a live server.


Setting it up
-------------

Activate your python virtual environment

    source ./venv/bin/activate

Make sure you have installed all dev requirements

    pip install -r requirements-dev.txt

Create the Silk tables in your local database

    python3 ./manage.py migrate

Run the server as normal

    python3 ./manage.py runserver

Use NearBeach as you normally would, then open the Silk interface at http://localhost:8000/silk/


What is configured
------------------

- silk is in INSTALLED_APPS, and silk.middleware.SilkyMiddleware is the first entry in MIDDLEWARE.
- silk.urls is mounted at /silk/ in local/urls.py.
- SILKY_PYTHON_PROFILER is True, which lets Silk collect a Python profile inside each profiled block.
- local/silk_profile_middleware.py wraps every request in silk_profile, named after the method and path. Without it
  the Profiling tab says "No Silk profiling was performed for this request", because Silk only profiles code that has
  been explicitly marked. The /silk/ pages are skipped so Silk does not profile itself.
- SILKY_MAX_RECORDED_REQUESTS, SILKY_MAX_REQUEST_BODY_SIZE and SILKY_MAX_RESPONSE_BODY_SIZE keep the Silk tables from
  growing without limit.


Reading the results
-------------------

1. The Requests page lists every request, newest first. Sort or filter by path, time taken or number of queries to find
   the slow ones.

2. Open a request, then its SQL tab, to see every query it ran with the time each one took. The same query repeated
   many times with different ids is an N+1 - fix it with select_related or prefetch_related.

3. The Profiling tab shows the Python call graph and timings for the whole request. Use it when the time is not in the
   database.

4. Timings include the profiling overhead, so compare requests against each other rather than trusting the absolute
   numbers.

5. When the list gets noisy, empty the Silk tables with the Clear DB option in the Silk menu, or from the command line

       python3 ./manage.py silk_clear_request_log


Profiling a specific piece of code
----------------------------------

To time one block in more detail, use the context manager or decorator from silk. For class based views, put the
decorator on the method, not the class.

    from silk.profiling.profiler import silk_profile

    with silk_profile(name='Build kanban payload'):
        ...

    @silk_profile(name='Project list')
    def get(self, request):
        ...


Turning it off
--------------

Remove silk, silk.middleware.SilkyMiddleware and local.silk_profile_middleware.SilkProfileAllRequestsMiddleware from
local/settings.py. The silk tables can stay in your local database.
