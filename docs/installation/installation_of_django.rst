.. _installation_of_django:

===================================
Installation of Django and Gunicorn
===================================


1. First update and upgrade the system so you are working with the latest packages;

  .. code-block:: bash

    sudo apt update && sudo apt upgrade -y


2. Next we will need to install all the packages we will use in NearBeach

  .. code-block:: bash

    sudo apt install python3-dev nginx curl build-essential python3-setuptools shared-mime-info libjpeg-dev zlib1g-dev

3. Install pip

  .. code-block:: bash

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python3 get-pip.py

4. After installing the required packages, you will need to update pip

  .. code-block:: bash

    sudo pip3 install --upgrade pip

5. Once pip is upgraded, you will need to create a virtual environment

  .. code-block:: bash

    sudo pip3 install virtualenv

6. Navigate to a directory where you would like to store your project. We would recommend /var/www/, if you require adding permission to /var/www/ please consult `Ubuntu Help <https://askubuntu.com/questions/19898/whats-the-simplest-way-to-edit-and-add-files-to-var-www#51337>`_ If you need to create your own project folder, then use the following commands

  .. code-block:: bash

    mkdir <<project_folder>>

  Then navigate into it

  .. code-block:: bash

    cd <<project_folder>>

7. Create your own virtual environment for python

  .. code-block:: bash

    virtualenv <<project_environment>>

  .. note:: Please do not use the name 'NearBeach' or variations of this for the Project Virtual Environment. Our recommended name would be 'venv'

  This will create a directory called "<<project_environment>>", this will store NearBeach's libraries for python

8. Activate the virtual environment using the following command

  .. code-block:: bash

    source ./<<project_environment>>/bin/activate

  You terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following

  .. code-block:: bash

    (<<project_environment>>)user@computer:

9. Install Django along with several other required packages

  .. code-block:: bash

    pip install django gunicorn

10. Django and gunicorn is now installed - we will now configure the webserver to server the pages.

11. Create a new django project

  .. code-block:: bash

    django-admin startproject <<django_project>>

  .. note:: Please do not create a project called 'NearBeach' as it will conflict with the NearBeach application. Our recommened name would be 'oceansuite'

12. Adjust the project's settings to allow debugging and accept ALL allowed hosts

  .. code-block:: bash

    nano ./<<django_project>>/<<django_project>>/settings.py

13. Change the following lines to reflect the following

  .. image:: images/django-installation-001.png

  This will allow us to test the web server. We will be modifying this file later to be more security conscience

  Save the settings file and exit

14. Test the django project can interact with gunicorn

  .. code-block:: bash

    cd ./<<django_project>>
    sudo ufw allow 8000
    gunicorn --bind 0.0.0.0:8000 <<django_project>>.wsgi

15. Now open up a new tab in your browser and go to;

  .. code-block:: bash

    https://<<your_domain_or_IP>>:8000

  You should see the following page load - note there will be no styling, that is fine as Gunicorn does not know how to find it.

  .. image:: images/django-installation-002.png

  If not, please check your error logs

------------------------------------------------
Installation of systemd Socket and Service files
------------------------------------------------

1. Gunicorn will need both socket and service files to be created to run automatically when the system starts.

2. Edit a gunicorn.socket file

  .. code-block:: bash

    sudo nano /etc/systemd/system/gunicorn.socket

3. Inside the file you will need the following code

  .. code-block:: bash

    [Unit]
    Description=gunicorn socket
    [Socket]
    ListenStream=/run/gunicorn.sock
    [Install]
    WantedBy=sockets.target

4. Save and close the file when you are finished

5. Edit a gunicorn.service file

  .. code-block:: bash

    sudo nano /etc/systemd/system/gunicorn.service

6. Inside the file you will need the following code

  .. code-block:: bash

    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=<<django_project_location>>
    ExecStart=<<virtualenv_location>>/bin/gunicorn \
      --access-logfile - \
      --workers 3 \
      --bind unix:/run/gunicorn.sock \
      <<django_project>>.wsgi:application
    [Install]
    WantedBy=multi-user.target

7. Save the file and exit

8. Run and test the socket

  .. code-block:: bash

    sudo systemctl start gunicorn.socket
    sudo systemctl enable gunicorn.socket

9. You will need to test the status of the gunicorn socket

  .. code-block:: bash

    sudo systemctl status gunicorn.socket

10. If gunicorn's status is active, you will need to configure nginx to proxy pass to gunicorn

11. Add your project file to sites-enabled

  .. code-block:: bash

    sudo nano /etc/nginx/sites-available/<<django_project>>

  Copy in the following text

  .. code-block:: bash

    server
    {
      listen 80;
      server_name <<your_domain_or_IP>>;
      location = /favicon.ico { access_log off; log_not_found off; }
      location /static/ { root <<django_project_location>>; }
      location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
      }
    }

12. Create a soft link

  .. code-block:: bash

    sudo ln -s /etc/nginx/sites-available/<<django_project>> /etc/nginx/sites-enabled

13. Test nginx

  .. code-block:: bash

    sudo nginx -t

  If there are errors at this point, consult the internet for a solution, or check the logs

  If no errors are reported, restart nginx

  .. code-block:: bash

    sudo systemctl restart nginx

14. Fix up the firewall

  .. code-block:: bash

    sudo ufw delete allow 8000
    sudo ufw allow 'Nginx Full'

15. Edit the settings file to limit the security

  .. code-block:: bash

    nano ./<<django_project>>/settings.py

  Fill out the Allowed host with an appropriate value(s), and turn off debug

16. Restart gunicorn ``sudo service gunicorn restart``

More information on this install can be found on `digital ocean's documentation <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04>`_

-----------------------
Installation of Certbot
-----------------------

Certbot is recommended by NearBeach to supply free certified SSL certificates. Please follow the instructions found on the `Certbot's Site <https://certbot.eff.org/>`_


-------------------------
Installation of XSendFile
-------------------------

.. note::

    Nginx might require user to setup XSendFile, please see more information here - https://www.nginx.com/resources/wiki/start/topics/examples/xsendfile/
