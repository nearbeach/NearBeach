.. _trouble_shooting_issues:

=======================
Trouble Shooting Issues
=======================

-----------------------------
PDF Rendering gives 500 error
-----------------------------

.. important:: Weasy print will sometimes express errors - this is due to library issues with Weasy print and can occur after an update. The best solution is to update Weasy print

The best solution at the moment is to update weasy print when you update your OS

1. Open up a terminal, and use Secure Shell (SSH) to log into your environment

2. Change directory to the location of the virtual environment's root folder is stored

  .. code-block:: bash

    cd /<<virtual_env_root>>

  .. note:: you do not have to change directory into the virtual environment folder


3. Activate your virtual environment

  .. code-block:: bash

    source ./<<virtual_env_folder>>/bin/activate

  .. note:: If you have changed directory into the virtual environment folder in the previous set, just modify the instructions to reflect that

4. Update pip, then weasy print

  .. code-block:: bash

    pip install -U pip
    pip install -U weasyprint


If the issues still persist, please consider updating your system and the pip packages

.. code-block:: bash

  sudo apt-get update && sudo apt-get upgrade -y
  pip install -U -r <<path_to_requirements.txt>>
