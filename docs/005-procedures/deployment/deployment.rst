.. _deployment:

=======================
Deployment of NearBeach
=======================

.. note::

    NearBeach uses Pypi and Docker to deploy to customers.

    `NearBeach on Pypi can be found here <https://pypi.org/project/NearBeach>`_

    `NearBeach on Docker can be found here <https://hub.docker.com/r/robotichead/nearbeach>`_


.. note::

    The following instructions will guide you on how to deploy NearBeach to both PyPi and Docker. Please follow the steps
    in order.


.. note::

    There is a current task opened to automate a lot of this process. These instructions will change in the future so please
    reference them before each deployment.


--------------------
Checklist and Method
--------------------

.. note::

    Follow this list in order


.. note::

    We are making sure you are in a terminal that is in the root folder of the project

#. Git pull and merge in the main branch. We want any security fixes in node packages

#. Run audit tools and fix any packages

#. Remove the `./build` and `./dist` folder

#. Update the version numbers in the following files

    * `./NearBeach/__init__.py`

    * `./package.json`

#. Make sure you are currently using the correct virtual environment; `source ./venv/bin/active`

#. Run the unit tests for the django backend to make sure nothing is broken; `python3 ./manage.py test`

#. Run the unit tests for the vue frontend to make sure nothing is broken; `npm run unit`

#. Compile the JavaScript into production mode; `npm run prod`

#. Implement the End to End tests using playwright; `npm run e2e`.
    Alternatively - if you would like to see UI for the tests use `npm run e2e-ui`

#. Edit the `setup.py` file if there are any new packages that need to be downloaded in the Docker File.

#. Update any virtualenv packages using the following commands
    `pip list --outdated`

    `pip install --upgrade <<package_name>>`

#. Run the following command to setup the dists file
    `python3 setup.py sdist bdist_wheel`

#. Run the following command to upload NearBeach Application to pypi
    `python3 -m twine upload dist/* --repository NearBeach`

#. Push the code back upstream

#. Do a pull request to merge code back into `main` branch

#. Create a new release off the new `main` branch. This process will trigger the deployment of static files to the CDN

#. Go the the https://github.com/robotichead/nearbeach-docker and edit the github actions file. Increase the version number. Pushing the code will cause github actions to build the latest docker build and release them.

