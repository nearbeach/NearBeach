.. _deployment:

=======================
Deployment of NearBeach
=======================

.. note::

    NearBeach uses Pypi and Docker to deploy to customers.

    `NearBeach on Pypi can be found here <https://pypi.org/project/NearBeach>`_

    `NearBeach on Docker can be found here <https://hub.docker.com/r/robotichead/nearbeach>`_


There are two release processes.

Process 1: should be used when there is new code for NearBeach, and any library updates

Process 2: should be used when there is a security issue within any of the libraries used for NearBeach. This will
deploy an update for those libraries without sending out any new NearBeach code. aka deploy separately from the
NearBeach deployment cycle.

i.e Boto3 has a security patch, and we need to deploy

--------------
Initial Checks
--------------

Check 1: If NearBeach requires any new Python Packages, these will need to be noted within the following locations;

NearBeach Source

- /requirements.txt
- /NearBeach/requirements.txt
- /.github/deployment_files/template_pyproject.toml

The above will make sure the Python package is installed in the Docker build of NearBeach.


Check 2: Make sure Docker will build and run

#. Using a terminal, cd into the NearBeach-Docker source directory

#. Do a simple git pull and check that you are on the correct branch

#. Run the following command to build a local version of NearBeach `docker build --no-cache --file Dockerfile --tag robotichead/nearbeach:nearbeach-local .`

#. Use the docker-compose example on https://nearbeach.org/self-hosting/ and save in an appropriate location as docker-compose.yml

#. Using the terminal, cd to the location of the docker-compose.yml file from previous instructions

#. Modify the NearBeach image to match the build name. `image: robotichead/nearbeach:nearbeach-local`

#. Using docker compose up -D you can easily test the local docker build of NearBeach


Check 3: Make sure Local Code will build and run

#. Use the docker-compose example on https://nearbeach.org/self-hosting/ and save in an appropriate location

#. Modify the Volumes to override the NearBeach installation directory - https://stackoverflow.com/questions/40905761/how-do-i-mount-a-host-directory-as-a-volume-in-docker-compose

TODO - Finish Check 3 code


--------------------
Deployment Process 1
--------------------


.. note::

    Please make sure you are in a terminal, that is in the root folder of the project.

#. Make sure you are on the develop branch, and all required features have been finished. i.e. merged into the develop
   branch.

#. Run audit tools and fix any packages

   .. code-block:: console

      npm audit


#. Compile the JavaScript into production mode

   .. code-block:: console

      npm run prod


#. Implement the End to End tests using playwright

   .. code-block:: console

      npm run e2e



   Please note - you'll need a default instance of NearBeach running with the fixture "NearBeach_basic_setup.json".

#. Check all screenshots from the End to End tests

#. Make sure the development branch has been pushed into origin. This will include the compilation of the production
   JavaScript

#. Check CircleCI's latest build status for the development branch. All tests should be passing. If there are any tests
   that have failed, they'll need to be fixed before deployment.

#. Using gitflow, we'll create a release.

   .. code-block:: console

      git flow release start <<version_number>>


   The version number should follow the format x.y.z. More information can be found at https://semver.org/

#. Using gitflow, we'll finish the release.

   .. code-block:: console

      git flow release finish <<version_number>>


#. Push both the dev and main branch into the origin.

#. Go to github, and do a release in github. Currently the release from the console does not trigger the github actions.

#. Check the github actions for NearBeach, to see if the workflows are running correctly.


--------------------
Deployment Process 1
--------------------

This process should ONLY be followed when we just want to deploy a new version of NearBeach's core libraries without
deploying any of the new code. i.e. separated from the development cycle.

Example 1: Boto3 has a security patch, we need to release this library into NearBeach's docker containers and get
everyone to use the newest versions.

#. Go to https://github.com/NearBeach/NearBeach

#. On the NearBeach github page, click on the "Create a new release"

#. Appropriately fill out the tag using the version x.y.z - for more information please read https://semver.org/

#. Fill out the rest of the information as approprately as possible. Explain why there is a release, i.e. security patch
   for external library

#. Make sure the target is "main"

#. Deploy the release