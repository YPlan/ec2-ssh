=======
ec2-ssh
=======

.. image:: https://img.shields.io/pypi/v/ec2-ssh.svg
    :target: https://pypi.python.org/pypi/ec2-ssh

.. image:: https://travis-ci.org/YPlan/ec2-ssh.svg?branch=master
    :target: https://travis-ci.org/YPlan/ec2-ssh


A pair of command line utilities for finding and SSH-ing into your Amazon EC2
instances by tag (such as 'Name').

Forked from Instagram original code by YPlan.

Installation
------------

From pip:

.. code-block:: sh

    pip install ec2-ssh

Usage
-----

There are two utilities: ``ec2-ssh`` and ``ec2-host``.

1. ``ec2-ssh``
~~~~~~~~~~~~~~

Use the ``ec2-ssh`` command to SSH into your instances. Rather than a hostname
to SSH into, it takes a tag key (default Name) and value, looks up the
instances matching that tag, randomly picks one (if there is >1) and uses its
public hostname, or private IP if it's not public. The username is defaulted to
``ubuntu``.

For example:

.. code-block:: sh

    $ ec2-ssh myapp
    # looks up instances where Name=myapp, expands out to something like:
    # ssh ubuntu@ec2-123-45-67-89.compute-1.amazonaws.com

    $ ec2-ssh root@myapp
    # expands to
    # ssh root@ec2-123-45-67-89.compute-1.amazonaws.com

You can pass the ``-t / --tag`` option to use a different tag key to search on,
for example:

.. code-block:: sh

    $ ec2-ssh -t role myapp-frontend

All other options are passed through to SSH so you can do things like:

.. code-block:: sh

    $ ec2-ssh myapp -- sudo systemctl restart nginx
    $ ec2-ssh -vvv myapp  # why can't I connect??


2. ``ec2-host``
~~~~~~~~~~~~~~~

This tool exposes just the host-lookup logic from ``ec2-ssh`` you can use it
for other purposes. The only difference is that rather than returning just one
matching instance's hostname/IP, it will return all of them. For example:

.. code-block:: sh

    $ ec2-host  # no tag, prints all instance hosts
    ec2-123-45-67-89.compute-1.amazonaws.com
    ec2-123-45-67-90.compute-1.amazonaws.com
    ec2-123-45-67-91.compute-1.amazonaws.com

    % ec2-host myapp  # only instances where Name=myapp
    ec2-123-45-67-89.compute-1.amazonaws.com
    ec2-123-45-67-90.compute-1.amazonaws.com

    % ec2-host -t environment prod  # instances where environment=prod
    ec2-123-45-67-90.compute-1.amazonaws.com
    ec2-111-45-67-90.compute-1.amazonaws.com
