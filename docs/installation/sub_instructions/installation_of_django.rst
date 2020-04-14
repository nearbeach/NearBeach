.. _installation_of_django:

===================================
Installation of Django and Gunicorn
===================================


1. First update and upgrade the system so you are working with the latest packages;

    sudo apt-get update && sudo apt-get upgrade -y


2. Next we will need to install all the packages we will use in NearBeach
  ``sudo apt install python3-dev libpq-dev nginx curl build-essential python3-setuptools libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info``

3. Install pip
  ``curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py``
  ``sudo python3 get-pip.py``

4. After installing the required packages, you will need to update pip
  ``sudo pip3 install --upgrade pip``

5. Once pip is upgraded, you will need to create a virtual environment
  ``sudo pip3 install virtualenv``

6. Navigate to a directory where you would like to store your project. We would recommend /var/www/, if you require adding permission to /var/www/ please consult `Ubuntu Help <https://askubuntu.com/questions/19898/whats-the-simplest-way-to-edit-and-add-files-to-var-www#51337>`_ If you need to create your own project folder, then use the following commands
  ``mkdir <<project_folder>>``

  Then navigate into it
  ``cd <<project_folder>>``

7. Create your own virtual environment for python

  ``virtualenv <<project_environment>>``

  This will create a directory called "<<project_environment>>", this will store NearBeach's libraries for python

8. Activate the virtual environment using the following command

  ``source ./<<project_environment>>/bin/activate``

  You terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following
  ``(<<project_environment>>)user@computer:``

9. Install Django along with several other required packages
  ``pip install django gunicorn``

10. Django and gunicorn is now installed - we will now configure the webserver to server the pages. Use the cd command to navigateYou terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following to the directory where you would like to store the django project

11. Create a new django project

  ``django-admin.py startproject <<django_project>>``

12. Adjust the project's settings to allow debugging and accept ALL allowed hosts

  ``nano ./<<django_project>>/<<django_project>>/settings.py``

13. Change the following lines to reflect the following

  ..image:: images/django-installation-001.png

  This will allow us to test the web server. We will be modifying this file later to be more security conscience

  Save the settings file and exit

14. Test the django project can interact with gunicorn
  ``cd ./<<django_project>>``
  ``sudo ufw allow 8000``
  ``gunicorn --bind 0.0.0.0:8000 <<django_project>>.wsgi``

15. Now open up a new tab in your browser and go to;

  ``https://<<your_domain_or_IP>>:8000``

  You should see the following page load - note there will be no styling, that is fine as Gunicorn does not know how to find it.

  ..image:: images/django-installation-002.png

  If not, please check your error logs

------------------------------------------------
Installation of systemd Socket and Service files
------------------------------------------------

1. Gunicorn will need both socket and service files to be created to run automatically when the system starts.

2. Edit a gunicorn.socket file
  ``sudo nano /etc/systemd/system/gunic``

  Your terminal prompt will change to indicate that it is working in the virtual environment now. It should look like the following
  ``(<<project_environment>>)user@computer:``

3. Inside the file you will need the following code
  ``[Unit]``
  ``Description=gunicorn socket``
  ``[Socket]``
  ``ListenStream=/run/gunicorn.sock``
  ``[Install]``
  ``WantedBy=sockets.target``

4. Save and close the file when you are finished

5. Edit a gunicorn.service file
  ``sudo nano /etc/systemd/system/gunicorn.service``

6. Inside the file you will need the following code
  ``[Unit]``
  ``Description=gunicorn daemon``
  ``Requires=gunicorn.socket``
  ``After=network.target``

  ``[Service]``
  ``User=www-data``
  ``Group=www-data``
  ``WorkingDirectory=<<django_project_location>>``
  ``ExecStart=<<virtualenv_location>>/bin/gunicorn \``
  ``  --access-logfile - \``
  ``  --workers 3 \``
  ``  --bind unix:/run/gunicorn.sock \``
  ``  <<django_project>>.wsgi:application``
  ``[Install]``
  ``WantedBy=multi-user.target``

7. Save the file and exit

8. Run and test the socket
  ``sudo systemctl start gunicorn.socket``
  ``sudo systemctl enable gunicorn.socket``

9. You will need to test the status of the gunicorn socket
  ``sudo systemctl status gunicorn.socket``

10. If gunicorn's status is active, you will need to configure nginx to proxy pass to gunicorn

11. Add your project file to sites-enabled
  ``sudo nano /etc/nginx/sites-available/<<django_project>>``
  Copy in the following text

  ``server``
  ``{``
  ``  listen 80;``
  ``  server_name <<your_domain_or_IP>>;``
  ``  location = /favicon.ico { access_log off; log_not_found off; }``
  ``  location /static/ { root <<django_project_location>>; }``
  ``  location / {``
  ``    include proxy_params;``
  ``    proxy_pass http://unix:/run/gunicorn.sock;``
  ``  }``
  ``}``

12. Create a soft link
  ``sudo ln -s /etc/nginx/sites-available/<<django_project>> /etc/nginx/sites-enabled``

13. Test nginx
  ``sudo nginx -t``

  If there are errors at this point, consult the internet for a solution, or check the logs

  If no errors are reported, restart nginx
  ``sudo systemctl restart nginx``

14. Fix up the firewall

  ``sudo ufw delete allow 8000``

  ``sudo ufw allow 'Nginx Full'``

15. Edit the settings file to limit the security

  ``nano ./<<django_project>>/settings.py``

  Fill out the Allowed host with an appropriate value(s), and turn off debug

16. Restart gunicorn ``sudo service gunicorn restart``

More information on this install can be found on `digital ocean's documentation <https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04>`_

-----------------------
Installation of Certbot
-----------------------

Certbot is recommended by NearBeach to supply free certified SSL certificates.

1. Install certbox
  ``sudo apt-get install python-certbot-nginx``

2. Once installed, run certbot
  ``sudo certbot --nginx``

Follow the prompts to install certbot. This will enable https to your NearBeach site.
