Automatic Testing
#################

NearBeach has the following automatic testing setup;

- Backend Unit Tests
- Frontend Unit Tests
- Frontend End-to-end tests
- Backend API Fuzzy Testing


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