DigitalOcean Firewalls IP changer
=================================

This personal project aims to give an easy and automated way to access resources created using the
DigitalOcean service, but blocked behind firewalls.
Especially during the current global crysis (great covid-19 pandemic of the 21st century), developers
need to work from home, and in order to access remote services they need to update the company's firewalls
with their updated ip.


Features
--------

* Automated removal of your old ip from the firewalls
* Automated addition of your new ip to the firewalls
* Easy to understand yaml config file, in which all the ip history is also kept

Installation
------------

This project requires python to be installed, and at least at version 3.6

This project works using poetry (https://python-poetry.org/docs/) to create a virtual environment
and not pollute system interpreters. Make sure to install it in order to use this project.

.. code-block::

    git clone https://github.com/HitLuca/digitalocean-firewalls-ip-changer
    cd digitalocean-firewalls-ip-changer
    poetry install

Running the project
-------------------

To run the project, simply

.. code-block::

    poetry run python digitalocean_firewalls_ip_changer/main.py

If it's your first time running the project, please check the info messages and update your config
file accordingly!

Contribute
----------

- Issue Tracker: https://github.com/HitLuca/digitalocean-firewalls-ip-changer/issues
- Source Code: https://github.com/HitLuca/digitalocean-firewalls-ip-changer

Support
-------

If you are having issues, please let me know. This is a personal project, but if general interest is
shown, I'll make sure to put more work into it

License
-------

The project is licensed under the MIT license.


Planned Features
----------------

* Allow updating multiple firewalls at once
* Improve how configuration files are handled
* Increase robustness by adding more checks