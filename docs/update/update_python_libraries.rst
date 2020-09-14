.. _update_python_libraries:

=======================
Update Python Libraries
=======================

NearBeach's python libraries will need to be updated for security and performance.


.. warning::

    Please try the updates on a non-production environment first. We can not stop 3rd party libraries from breaking your
    server environment.


------
Method
------

1. You will need to be in your virtual environment

  .. code-block:: bash

    source <<virtualenv_location>>/bin/activate


2. Find out which libraries need to be updated

  .. code-block:: bash

    pip list --outdated

  Take note which packages need to be updated.


3. Use the following command to update the packages

  .. code-block:: bash

    pip install --upgrade <<package_name>>

  Run this for ALL packages, please note you can string the packages into one command.

  .. code-block:: bash

    pip install --upgrade django pillow


.. note::

  Do not use the above method to update NearBeach. Please follow the instructions located in chapter "Update Or Patch
  NearBeach"