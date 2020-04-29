DigitalOcean Firewalls IP changer
=================================

.. image:: https://travis-ci.com/HitLuca/digitalocean-firewalls-ip-changer.svg?branch=master
    :target: https://travis-ci.com/HitLuca/digitalocean-firewalls-ip-changer

.. image:: http://hits.dwyl.com/HitLuca/digitalocean-firewalls-ip-changer.svg
    :target: http://hits.dwyl.com/HitLuca/digitalocean-firewalls-ip-changer

This personal project aims to give an easy and automated way to access resources created using the
DigitalOcean service, but blocked behind firewalls.
Especially during the current global crysis (great covid-19 pandemic of the 21st century), developers
need to work from home, and in order to access remote services they need to update the company's firewalls
with their updated ip.


Features
--------

* Automated removal of your old ip from the firewalls
* Automated addition of your new ip to the firewalls
* Supports creating a firewall rule for multiple ports
* Easy to understand yaml config file, in which all the ip history is also kept

Installation
------------

This project requires python to be installed, and at least at version 3.6

This project works using poetry (https://python-poetry.org/docs/) to create a virtual environment
and not pollute system interpreters. Make sure to install it in order to use this project.

This project also requires doctl, a DigitalOcean cli interface. For this reason, first do the following:

* Install Doctl to use the DigitalOcean APIs (https://github.com/digitalocean/doctl/blob/master/README.md)
* Log in to the DigitalOcean service using doctl

A guide that describes all the features of doctl can be found `here <https://www.digitalocean.com/community/tutorials/how-to-use-doctl-the-official-digitalocean-command-line-client>`_.
After doctl is installed, install the project by running:

.. code-block:: bash

    git clone https://github.com/HitLuca/digitalocean-firewalls-ip-changer
    cd digitalocean-firewalls-ip-changer
    poetry install


Running the project
-------------------

To run the project, simply

.. code-block:: bash

    poetry run python digitalocean_firewalls_ip_changer/main.py

If it's your first time running the project, please check the info messages and update your config
file accordingly!

The config file
---------------

In order to store all the past ips (for reference), the firewall settings, and everything that could be needed,
this project uses a yaml configuration file

``config.yaml``

.. code-block:: yaml

    firewall_id: 123-456-abc-def
    last_ip: 11.11.11.11
    past_ips:
        - 22.22.22.22
        - 33.33.33.33
    ports:
        - 80
        - 443
        - 8081
    protocol: tcp

* The ``firewall_id`` indicates the DigitalOcean id assigned to the firewall you want to update
* ``last_ip`` is the last ip recorded, usually your current one
* ``past_ips`` are all the past ips you had, for reference, should any issues arise
* ``ports`` are the ports you will need to use as a remote developer, in this example ``80 443 8081``
* ``protocol`` should be kept equal to ``tcp``

How to the firewall_id
----------------------

If the firewall which requires updates hasn't been renamed from its original id, congratulations! This
is the id you need to use (an example id is ``abc-12b123jl-34k2-3j1n-532j-as234jlb2``)

If the firewall id has been updated to something different than the original, then you need to retrieve it:

* List your firewalls, using ``doctl compute firewall list``
* Find your firewall_id

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

* Ensure that doctl is installed before running any operations
* Allow updating multiple firewalls at once
