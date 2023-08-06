Batch Emailer
==========================

This is a plugin for `pretix`_. 
It allows you to send Emails to all orders, which are currently displayed. 

Use the filters in the order view, the question answer page, ... to select the group of orders you want to adress. 

.. warning::
    This plugin doesn't support pagination. It grabs all currently rendered order links, this excludes all orders on the next and previous pages.
    Currently you have to send the same email multiple times, once for each page.

.. image:: docs/Button.png
  :width: 400
  :alt: Pretix Control view with an additional button in the top header. It has the label "Batch email visible orders".

The Button "Batch email visible orders" preloads an email composition view with all these orders.

.. image:: docs/ComposeMails.png
  :width: 400
  :alt: Email composition interface

There exists a seperate history for all batch emails.

.. image:: docs/History.png
  :width: 400
  :alt: Send email history for batch emails.



Development setup
-----------------

1. Make sure that you have a working `pretix development setup`_.

2. Clone this repository.

3. Activate the virtual environment you use for pretix development.

4. Execute ``python setup.py develop`` within this directory to register this application with pretix's plugin registry.

5. Execute ``make`` within this directory to compile translations.

6. Restart your local pretix server. You can now use the plugin from this repository for your events by enabling it in
   the 'plugins' tab in the settings.

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed::

    pip install flake8 isort black docformatter

To check your plugin for rule violations, run::

    docformatter --check -r .
    black --check .
    isort -c .
    flake8 .

You can auto-fix some of these issues by running::

    docformatter -r .
    isort .
    black .

To automatically check for these issues before you commit, you can run ``.install-hooks``.


License
-------


Copyright 2021 Lukas Bockstaller

Released under the terms of the Apache License 2.0



.. _pretix: https://github.com/pretix/pretix
.. _pretix development setup: https://docs.pretix.eu/en/latest/development/setup.html
