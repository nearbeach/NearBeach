.. _local_development_environment:

=============================
Local Development Environment
=============================

| The steps outlined here are to setup this project in local environment so that you can edit the project and test in your local. 
| If you are want to have a demo or deploy this project. Please head over to :ref:`quick-install-docker`.

.. warning:: 
  This setup is not intended for production environments and do not follow these steps in UAT, DEV, PROD or any other non local environments. The :code:`local/settings.py` file contains a secret_key which will be a security concern.


Contents: 

.. contents::
   :local:
   :depth: 1

------------
Prerequsites
------------

| The following prerequisites are required to run this project on your local machine.

Install python 3.7+
####################

    | Run the following command to check the installed python version
  
      .. code-block:: bash

        python3 --version

    | If you have not installed Python 3.7+ on your local machine, head over to https://www.python.org/downloads/ and download latest version of Python.

Install Git
###########

  | Run the following command to check the installed git version.
    
    .. code-block:: bash

      git --version

  | If you have not installed Git on your local machine, head over to https://git-scm.com/downloads and download the latest version of Git.

Install pip
###########

  | Run the following command to check the installed pip version.
    
    .. code-block:: bash

      pip3 --version

  | If you have not installed Pip on your local machine, head over to https://pip.pypa.io/en/stable/installation/ and download the latest version of pip.

Install npm
###############

  | Run the following command to check the installed npm version.
    
    .. code-block:: bash

      npm --version

  | If you have not installed npm on your local machine, head over to https://nodejs.org/en/download/ and download the latest version of npm and Node.js.

-----------------------
Setting up the project
-----------------------

  1. | Head over to https://github.com/nearbeach/NearBeach and fork the repository to your own github account. You can skip this step if dont want to fork.


  2. Open a terminal, navigate to a folder where you want to setup this project

    .. code-block:: bash

      cd /path/to/your/project/folder

  3. Download the project from the forked repository. Copy the link from the forked repository and run the following command in the terminal.

    .. code-block:: bash

      git clone <<Forked repo URL here>>
      cd ./NearBeach

    If you have not forked the repository, you can clone the main repository using the following command

    .. code-block:: bash

      git clone https://github.com/nearbeach/NearBeach.git
      cd ./NearBeach

  4. Download and install virtualenv

    .. code-block:: bash

      sudo pip3 install virtualenv

  5. Create your own virtual environment for python
    
    .. note::
      you can use any name for the virtual environment, but it is recommended to use "venv" as it is already added to the .gitignore file
      
    .. code-block:: bash

      virtualenv venv
    
    This will create a directory called "venv" in your current directory, this will store the required python libraries for the project

  6. Activate the virtual environment

    .. code-block:: bash

      source ./venv/bin/activate

    You terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following:

      .. code-block:: bash
        
        (venv)user@computer NearBeach$:

  7. Install the python libraries
    
    This will install all the required python libraries for the project

    .. code-block:: bash

      pip install -r requirements-dev.txt

  8. Create the database

    .. code-block:: bash

      python3 manage.py migrate

  9. Create a superuser for the application

    | Execute the following command and fill the user details when prompted.
    | This user will act as super user for the NearBeach application. Use this user to login to the website once the Django app runs.

    .. code-block:: bash
    
      python3 manage.py createsuperuser

  10. Run the Django webserver

    .. code-block:: bash
    
      python3 manage.py runserver

    Alternatively, you can run the server on a different port using the following command

    .. code-block:: bash

      python3 manage.py runserver <<Port number>>

    .. attention::
      
      If you see an error message like "DisallowedHost at /", you need to add 127.0.0.1 to the allowed hosts in the :code:`local/settings.py` file. 
      Open :code:`local/settings.py` file and add :code:`127.0.0.1` to the ALLOWED_HOSTS list

      .. code-block:: python

        ALLOWED_HOSTS = ['127.0.0.1']

  If all the above steps are followed correctly you should see the following output:

    .. code-block:: bash

      Performing system checks...

      System check identified no issues (0 silenced).
      October 27, 2024 - 12:00:00
      Django version 3.2.8, using settings 'NearBeach.settings'
      Starting development server at http://127.0.0.1:8000/
      Quit the server with CONTROL-C.

  .. note::
    | Now that the server is running, you can access the NearBeach login page by visiting http://127.0.0.1:8000/login
    | You can also access the Django admin page by visiting http://127.0.0.1:8000/admin

--------------
NPM/JavaScript
--------------

  1. To install all NPM packages, please run the following code

    .. code-block:: bash

      npm install

  2. Once npm has finished installing, compile the code using the following command

    .. code-block:: bash

      npm run prod

  3. Alternatively, you can run a watch

    .. code-block:: bash

      npm run watch

----------------  
Whats next
----------------
  
  Now the road is clear for you to start contributing.
  
  Head over to :code:`local/NearBeach` folder. This is where all the python code is stored.

  .. warning::
    | DO NOT modify :code:`local/settings.py`! 
    | Before commiting the code please revert back the changes that are made to :code:`local/settings.py` file.


  .. seealso:: 
    Hop on to our discord server - https://discord.gg/64uhRztS6n

