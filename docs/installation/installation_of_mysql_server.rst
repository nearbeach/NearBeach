.. _installation_of_mysql_server:


============================
Installation of MySQL Server
============================

The following quick instructions will inform you on how to install MySQL in Ubuntu for NearBeach. This will also cover the generation of the NearBeach user for the database

1. Install the following packages

  .. code-block:: bash

    sudo apt-get install mysql-server mysql-client libmysqlclient-dev

2. Once installation of the mysql-server has been completed, setup your root user

  .. code-block:: bash

    sudo mysql_secure_installation

3. Follow the prompts with creating a root user, we had the following answers

4. Once mysql has been completely, log into mysql to install the NearBeach user

  .. code-block:: bash

    sudo mysql -u root -p

  enter in the root password for MySQL

5. Create the new nearbeach user

  .. code-block:: bash

    CREATE USER 'nearbeach'@'localhost' IDENTIFIED BY '<<password>>';

  
  Create the database NearBeach
  
  .. code-block:: bash

    CREATE DATABASE NearBeach;
    
  
  Grant the nearbeach user access to the NearBeach database

  .. code-block:: bash

    GRANT ALL PRIVILEGES ON NearBeach.* TO 'nearbeach'@'localhost';
  

  Flush all priveledges
  
  .. code-block:: bash
  
    FLUSH PRIVILEGES;
  

  Exit mysql
  
  .. code-block:: bash

    exit


6. Edit the django project settings file to allow your django project access to the mysql database

  .. code-block:: bash

    cd <<django_project_location>>
    nano ./<<django_project>>/settings.py

7. Add the following code into the database section of the settings file

  .. code-block:: bash

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '<<mysql database>>',
            'USER': '<<mysql username>>',
            'PASSWORD': '<<mysql password>>',
            'HOST': 'localhost', # Or an IP Address that your DB is hosted on
            'PORT': '3306',
        }
    }

8. Restart gunicorn

  .. code-block:: bash

    sudo service gunicorn restart

9. Migrate the basic Django admin tables to the database

  .. code-block:: bash

    source <<virtualenv_location>>/bin/activate
    pip install mysqlclient
    cd <<django_project_location>>
    ./manage.py migrate

10. Create the super user for the Django Project

  .. code-block:: bash

    ./manage.py createsuperuser

  Follow the prompts to create the superuser

11. Test your Django project by visiting your site

  .. code-block:: bash

    https://<<your_domain_or_IP>>

You should now have a blank page.
