================================
Ubuntu 18.04 Server Installation
================================

-------------------------------
Minimum requirements - Hardware
-------------------------------

* 1GB RAM
* 1+ Core CPU (for small user base)
* 5+ GB Space (more for uploading documents)

-------------------------------
Minimum requirements - Software
-------------------------------

* Ubuntu 18.04
* Python 3.6+
* Django 2.1+
* Nginx
* Gunicorn
* MySQL

The following instructions will allow you to install Ubuntu 18.04 on your server.
These are just the quick steps and do not go into detail. If you wish to go into
more detail please visit the Ubuntu help site -
`https://help.ubuntu.com/lts/serverguide/ <https://help.ubuntu.com/lts/serverguide/>`_

Section 1 - Installation of Server
----------------------------------

Ubuntu 18.10

Section 2 - Installation of a Django and the setup of Gunicorn
--------------------------------------------------------------

Installation of Django

Section 3 - Setup of Database
-----------------------------

MySQL in Ubuntu

Section 4 - Installation of NearBeach
-------------------------------------

Installation of NearBeach

Optional Steps
--------------

Installation of Logs in NearBeach

Installation of NearBeach API

Connect Mapbox

Connect Google Maps

Trouble Shooting Issues
-----------------------

PDF Rendering gives 500 error

    Go to Ubuntu and download Ubuntu Server 18.04 - https://ubuntu.com/download/server
    Once downloaded, use any tools available to write the image to a USB (alternatively a CD/DVD)
        Windows - https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-windows
        Mac - https://tutorials.ubuntu.com/tutorial/tutorial-create-a-usb-stick-on-macos
        Linux - https://www.linux.com/blog/how-burn-iso-usb-drive
        Alternative Linux - Use the 'Disks' program to restore disk image to USB (easiest option)
    Boot up from USB on Server and choose your preferred language
    Choose the keyboard layout
    Choose the type of Ubuntu server you are after, i.e. Bare metal as a service
    Configure you network - click the "Done" button if there is nothing to change
    Configure the proxy - click "Done" if there is no proxy
    Configure the Ubuntu Archive mirror - click "Done" if there is no change
    Configure your file partition - click the "Done" if you are happy with the default. Please refer to the Ubuntu help docs for partitioning at the top of the page
    Setup your default user profile
    You will not need to install any snap objects - once completed the installation should start
