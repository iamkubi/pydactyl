pydactyl
========

An easy to use Python wrapper for the Pterodactyl Panel API.

.. toctree::
    :hidden:

    self

Documentation
=============
This documentation is generated from docstrings so the class names do
not usually match the way they are accessed when using PterodactylClient.

For example the `get_server()` method documented in the
`pydactyl.api.client.servers.base.ServersBase` class is accessed by calling
`client.servers.get_server()`.

The majority of names in PterodactylClient match their path minus the class
name, so `pydactyl.api.client.account.Account.get_server()` is
`client.account.get_server()`.  Classes named or ending with Base are
imported into the parent namespace.

More example usage can be found can be found in the README at
https://github.com/iamkubi/pydactyl.

Client API
==========
The Client API are endpoints available to any Pterodactyl user account and
require a Client API key generated in the account settings.

.. toctree::
    :maxdepth: 1
    :caption: client

    clientapi

Application API
===============
Application API endpoints are only available to Pterodactyl Administrators
and require an Application API key generated in the Admin panel.

.. toctree::
    :maxdepth: 1
    :caption: application

    applicationapi

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
