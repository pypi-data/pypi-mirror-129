============
Installation
============

This are the instructions to install Libervia Pubsub.

.. note::

   This documentation is work in progress

.. note::

    /!\\ Beware, if you're installing Libervia Pubsub on a server already running in production,
    it will replace your legacy Pubsub service, meaning that everything stored there won't
    be available anymore (this includes, and is not limited to, bookmarks, encryption
    keys, blogs, etc.).

    Be sure to save everything from your legacy Pubsub service before switching to Libervia
    Pubsub.

    Migration scripts are not yet available, help is welcome to write them.


Requirements
------------

- Python 3.7+
- Python 3 "venv", which may be installed with Python 3
- Mercurial
- A XMPP server that supports the component protocol (XEP-0114),
  and, to enable the micro-blogging feature, Namespace Delegation (XEP-0355)
  and privileged entity (XEP-0356) are needed.
  We recommend using Prosody with mod_privilege and mod_delegation modules (those modules
  are maintained by us).

For the PostgreSQL backend, the following is also required:

- PostgreSQL >= 9.5 (including development files for psycopg2)

Installation of dev version
---------------------------

First install system requirements. On a Debian system or derivative, you can use following
instructions::

    sudo apt-get install postgresql python3-dev python3-venv python3-wheel mercurial

Now go in a location where you can install Libervia Pubsub, for instance your home directory::

    $ cd

You'll need to create and activate a Python virtual environment::

    $ python3 -m venv pubsub-venv
    $ source pubsub-venv/bin/activate
    $ pip install -U pip wheel

Then you need to clone the repository::

    $ hg clone https://repos.goffi.org/sat_pubsub && cd sat_pubsub

Now you can install requirements::

    $ pip install -r requirements.txt

And that's it! Please refer to `Post Installation`_ to initialize database.

Next time you can update with::

    $ hg pull -u

.. note::

    if requirements change, you may have to enter ``pip install -r requirements.txt``
    again, check also `Update`_ below)

Installation From Sources
-------------------------

To install Libervia PubSub we'll work in a virtual environment. On Debian and derivatives you
should easily install dependencies with this::

    sudo apt-get install postgresql python3-dev python3-venv python3-wheel mercurial

Now go in a location where you can install Libervia Pubsub, for instance your home directory::

    $ cd

And enter the following commands::

    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -U pip wheel
    $ pip install sat-pubsub

.. note::

   If your are installing from a local clone of the repository, it has been reported that
   installation with ``python setup.py install`` is not working properly. Please use ``pip
   install .`` instead.

Post Installation
-----------------

Once Libervia Pubsub is installed, you'll need to create a PostgreSQL user, and create the
database::

    % sudo -u postgres createuser -d -P $(whoami)
    % createdb pubsub
    % cd /tmp && wget https://repos.goffi.org/sat_pubsub/raw-file/tip/db/pubsub.sql
    % psql pubsub < pubsub.sql

Update
------

If you have updated Libervia Pubsub and the database schema has been changed, you may have a
message indicating that your are using an outdated version.

To update schema, just apply ``sat_pubsub_update_x_y.sql`` files where ``x`` is your
current version, and ``y`` is the one to update. If you are several versions late, just
apply updates one by one.

For instance, if you have the following message::

    ERROR:root:Bad database schema version (7), please upgrade to 8

Go to ``db`` directory and enter update instruction::

    $ cd db
    $ psql pubsub < sat_pubsub_update_7_8.sql

.. note::

    Before any update and specially if there is a schema change, you should backup your
    database. If anything goes wrong, it will be your best chance to avoid any data loss.


.. _prosody_configuration:

Prosody Configuration
---------------------

Libervia PubSub can work with any XMPP server (which supports components), but if you want to
use it as your PEP service, you need a server which supports `XEP-0355`_ and `XEP-0356`_.

Below you'll find the instruction to use Libervia PubSub as a PEP service with Prosody:

-  add these two lines at the end of your ``prosody.cfg.lua`` file, adapting them to your XMPP
   server domain (virtual host) and selecting a password of your choice:

.. sourcecode:: lua

    Component "pubsub.<xmpp_domain>"
            component_secret = "<password>"

-  there are extra steps to enable the micro-blogging feature with Prosody. Please follow
   the installation and configuration instructions that are given on these pages:

   - https://modules.prosody.im/mod_delegation.html
   - https://modules.prosody.im/mod_privilege.html

To keep your modules up to date, we recommend to clone the full modules
repository and then to symlink them like that:

.. sourcecode:: shell

    % cd /path/to/install_dir
    % hg clone https://hg.prosody.im/prosody-modules
    % cd /path/to/prosody_plugins
    % ln -sf /path/to/install_dir/prosody-modules/mod_delegation ./
    % ln -sf /path/to/install_dir/prosody-modules/mod_privilege ./

Or course, you have to adapt ``/path/to/install_dir`` to the directory where you want to
install the modules, and ``/path/to/prosody_plugins`` to the directory where prosody
modules are installed (hint: check ``prosodyctl about`` to find the latter). The ``ln``
commands may have to be run as root depending on your installation.

Once your symlinks are set, to update the modules we just need to type this:

.. sourcecode:: shell

    % cd /path/to/install_dir/prosody-modules
    % hg pull -u

Here is an example of how your ``prosody.cfg.lua`` should look like with
``mod_delegation`` and ``mod_privilege`` activated:

.. sourcecode:: lua

    [...]
    modules_enabled = {
                  [...]
                  "delegation";
                  "privilege";
    }
    [...]
    VirtualHost "<xmpp_domain>"
      privileged_entities = {
        ["pubsub.<xmpp_domain>"] = {
          roster = "get";
          message = "outgoing";
          presence = "roster";
        },
      }
      delegations = {
          ["urn:xmpp:mam:2"] = {
            filtering = {"node"};
            jid = "pubsub.<xmpp_domain>";
          },
            ["http://jabber.org/protocol/pubsub"] = {
            jid = "pubsub.<xmpp_domain>";
          },
            ["http://jabber.org/protocol/pubsub#owner"] = {
            jid = "pubsub.<xmpp_domain>";
          },
            ["https://salut-a-toi/protocol/schema:0"] = {
            jid = "pubsub.<xmpp_domain>";
          },
            ["https://salut-a-toi.org/spec/pubsub_admin:0"] = {
            jid = "pubsub.<xmpp_domain>";
          },
            ["urn:xmpp:delegation:2:bare:disco#info:*"] = {
            jid = "pubsub.<xmpp_domain>";
          },
            ["urn:xmpp:delegation:2:bare:disco#items:*"] = {
            jid = "pubsub.<xmpp_domain>";
          },
      }

    Component "pubsub.<xmpp_domain>"
       component_secret = "<password>"
       modules_enabled = {"delegation", "privilege"}

Of course, you still have to replace and adapt to your own settings.

.. _XEP-0355: https://xmpp.org/extensions/xep-0355.html
.. _XEP-0356: https://xmpp.org/extensions/xep-0356.html

Running Libervia PubSub
-----------------------

The minimal example for running sat_pubsub is:

  % twistd sat-pubsub

This will start the service and run it in the background. It generates a
file twistd.pid that holds the PID of the service and a log file twistd.log.
The twistd utility has a fair number of options that might be useful, and
can be viewed with:

  % twistd --help

When the service starts, it will connect to the XMPP server at the local machine using the
component protocol, and assumes the JID ``pubsub``. This assumes a couple of defaults
which can be overridden by passing parameters to the twistd plugin. You can get an
overview of the parameters and their defaults using:

  % twistd sat-pubsub --help

In particular, the following parameters will be of interest:

 ``--jid``
    The Jabber ID the component will assume.

 ``--rport``
    the port number of the XMPP server to connect to

 ``--xmpp_pwd``
    the secret used to authenticate with the XMPP server.

For example::

  twistd sat-pubsub --jid=pubsub.<your_xmpp_domain> --xmpp_pwd=<password>

You can set your options in ``sat.conf`` which is the same file used as for Salut à Toi
ecosystem. Please check backend ``configuration`` section for details. The Libervia PubSub
options must be in ``[pubsub]`` section.
