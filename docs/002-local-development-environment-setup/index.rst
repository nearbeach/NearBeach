.. _local_development_environment:

=============================
Local Development Environment
=============================

  .. warning:: DO NOT use this method for ANY UAT/DEV/PROD environments that are NOT on your local. The settings.py file contains a secret_key that is published.

  .. warning:: DO NOT edit the settings.py file - as changes can be pushed to a public github.

  .. attention:: If you would like any help setting up these environments, why not join our discord - https://discord.gg/64uhRztS6n

NearBeach currently supports the following Django versions;

- Django Version 3.2+

More information about upgrading Django can be found `found in the Django Documentation <https://docs.djangoproject.com/en/3.0/howto/upgrade-version/>`_

  .. attention:: We are assuming you have pip3 installed on your local system. If not, please follow these instructions: https://github.com/pypa/get-pip

  .. attention:: We are assuming you have installed Python 3.7+ on your local development system. If not, please follow these instructions: https://www.python.org/downloads/


-----------------------
Download Git Repository
-----------------------

#. In a terminal, navigate to your project development folder

  .. code-block:: bash

    cd /<<project-dev-folder>>

#. Use Git to download NearBeach source code

  .. code-block:: bash

    git clone https://github.com/robotichead/NearBeach
    cd ./NearBeach

#. Once pip is upgraded, you will need to create a virtual environment

  .. code-block:: bash

    sudo pip3 install virtualenv

#. Create your own virtual environment for python

  .. code-block:: bash

    virtualenv <<project_environment>>

  This will create a directory called "<<project_environment>>", this will store NearBeach's libraries for python

#. Activate the virtual environment using the following command

  .. code-block:: bash

    source ./<<project_environment>>/bin/activate

  You terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following

  .. code-block:: bash

    (<<project_environment>>)user@computer:

#. Install All requirements

  .. code-block:: bash

    pip install requirements-dev.txt

#. Create the database

  .. code-block:: bash

    python3 manage.py migrate

#. Create a superuser, by running the following command and filling out the fields appropriately

  .. code-block:: bash
  
    python3 manage.py createsuperuser

#. Run the webserver

  .. code-block:: bash
  
    python3 manage.py runserver

#. To access NearBeach, open up your browser and go to `http://localhost:8000` or alternatively `http://127.0.0.1:8000`.

--------------
NPM/JavaScript
--------------

#. To install all NPM packages, please run the following code

  .. code-block:: bash

    npm install

#. Once npm has finished installing, you can compile the code using the following;

  .. code-block:: bash

    npm run prod

#. Alternatively, you can run a watch

  .. code-block:: bash

    npm run watch
