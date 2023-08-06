|Build Status| |Coverage| |Black|

tlsmate_client_simul
####################


Overview
========

This project provides a plugin for the `tlsmate application
<https://gitlab.com/guballa/tlsmate>`_. It allows to check the interoperability
of the chosen TLS server with multiple popular and well known TLS clients. In
case the simulated client can successfully connect to the server, the following
information negotiated between the client and the server is provided:

* TLS protocol version

* cipher suite

* the type of the key exchange including the key size or the supported group

* the server authentication mechanism including the key size

By default the parameters mentioned above will be colored according to the
chosen style.

Basically this plugin does the same than the client simulation by SSLAB's `SSL
Server Test <https://www.ssllabs.com/ssltest/>`_, and indeed this plugin uses
the `client date base <https://api.ssllabs.com/api/v3/getClients>`_ from this
site.


Installation
============

This package requires Python3.6 or higher. The recommended way installing this
``tlsmate`` plugin is using pip:

.. code-block:: console

    $ pip install tlsmate_client_simul

Note: If required, the ``tlsmate`` application will be installed as well.


Basic usage
===========

This plugin can be used in two different ways.


Using the client-simul subcommand
---------------------------------

The plugin extends ``tlsmate`` by the new subcommand ``client-simul``. This
allows to perform this client simulation independently from any other scan
options ``tlsmate`` provides.

Here is an example:

.. code-block:: console

   $ tlsmate client-simul --progress mytlsmatedomain.net

Some basic parameters from tlsmate's ``scan`` command are supported, use the
``--help`` argument to display all the available command line options:

.. code-block:: console

   $ tlsmate client-simul --help


Extending a server scan
-----------------------

The plugin can also be used to extend a TLS server scan. To do so
the argument ``--client-simul`` must be given to the ``scan`` subcommand:

.. code-block:: console

   $ tlsmate scan --progress --client-simul mytlsmatedomain.net


Note: In the examples above the domain name "mytlsmatedomain.net" is used,
which is currently not registered. Replace it with the domain name you want to
use.

.. |Build Status| image:: https://gitlab.com/guballa/tlsmate_client_simul/badges/master/pipeline.svg
   :target: https://gitlab.com/guballa/tlsmate_client_simul/-/commits/master

.. |Coverage| image:: https://gitlab.com/guballa/tlsmate_client_simul/badges/master/coverage.svg
   :target: https://gitlab.com/guballa/tlsmate_client_simul/-/commits/master

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
