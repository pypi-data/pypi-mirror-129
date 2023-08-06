.. _components:

===================
Libervia Components
===================

Libervia can act as an XMPP server component, which can be seen as a generic plugin for
XMPP servers.

This page explains which components are available and how to use them.

Running a component
===================

Components are linked to a Libervia profile in the same way as normal clients.

To run a component, you'll need to know its *entry point*, which is the name of the import
name of plugin managing it. The entry point to use will be specified in the component
installation documentation.

You'll also have to declare the component on your XMPP server, this is a server dependent
step and you'll have to check your server documentation for details. You'll have to
specify a **shared secret** (can also be named simply *password*) that must be set both on
the XMPP server and as the XMPP password of the Libervia profile.

Here is a list of relevant documentation for most common servers:

ejabberd
  https://docs.ejabberd.im/admin/configuration/listen-options/

MongooseIm
  https://esl.github.io/MongooseDocs/latest/configuration/listen/#xmpp-components-listenservice

OpenFire
  use the web-based admin panel

Prosody
  https://prosody.im/doc/components

Tigase
  https://docs.tigase.net/tigase-server/stable-snapshot/Administration_Guide/webhelp/externalComponentConfiguration.html


On Libervia, setup is done with Libervia CLI's :ref:`profile create <li_profile_create>`
command.

You'll usually want to have the component to start automatically when the backend
is started, for this you must unset the profile password (not to be confused with the XMPP
password which is the one also set on the server configuration) with ``-p ""`` and set
auto-connection with ``-A``.

You'll specify the XMPP password (also named *shared secret* in `XEP-0144`_ terminology)
with ``-x <your_shared_secret>`` and the JID to use with ``-j
<component_subdomain>.<server.tld>``.

The component entry point is specified with ``-C <entry_point>``.

.. _XEP-0144: https://xmpp.org/extensions/xep-0114.html

example
-------

Louise wants to run an ActivityPub gateway on her server ``example.org`` with the JID
``ap.example.org``. The shared secret is ``xmpp_rocks`` and she wants the component to
start automatically with the backend, thus she doesn't set a profile password. The
entry-point for ActivityPub component is ``ap-gateway``, and she wants to use the same
name for the profile. To do this, she enters the following command::

  $ li profile create ap-gateway -j ap.example.org -p "" -x xmpp_rocks -C ap-gateway -A

The component will then be started next time Libervia Backend is launched. If Louise
wants to connect it immediately, she can use::

  $ li profile connect -cp ap-gateway

Available Components
====================

Below is a list of currently available components in Libervia, and instructions on what
they do and how to use them.


File Sharing
------------

**entry_point:** ``file-sharing``

File Sharing component manage the hosting of user files. Users can upload file there using
either `Jingle File Transfer`_ or `HTTP File Upload`_.

There is no limit to the size of files which can be uploaded, but administrators can set a
quota to limit the space that can be used.

Files can be retrieved using `File Information Sharing`_, and deleted using `Ad-Hoc Commands`_.

Files can be shared with a public HTTP link, or made available only to a specified list of
entities (JIDs). Permissions can be set through Ad-Hoc Commands.

.. _Jingle File Transfer: https://xmpp.org/extensions/
.. _HTTP File Upload: https://xmpp.org/extensions/xep-0363.html
.. _File Information Sharing: https://xmpp.org/extensions/xep-0329.html
.. _Ad-Hoc Commands: https://xmpp.org/extensions/xep-0050.html

Configuration
~~~~~~~~~~~~~

All options are to be set in ``[component file-sharing]`` section.

``http_upload_port``
  port to use for HTTP File Upload

  **default**: 8888

``http_upload_connection_type``
  either ``http`` or ``https``.

  **default**: ``https``

  Note that HTTP Upload should always be ``https`` to end-user, the ``http`` option is to
  be used only if you use a HTTP server as a proxy, and this server is already set for
  TLS.

``http_upload_public_facing_url``
  must be set to the URL that end-user will see. Notably useful if the component is behind
  a proxy.

  **default**: ``https://<component host>:<http_upload_port``

``quotas_json``
  a JSON object indicating quotas to use for users. The object can have 3 keys:

  ``admins``
    quotas to use for administrators (i.e. profiles set in ``admins_list``)

  ``users``
    quotas to use for normal users (i.e. non admin profiles)

  ``jids``
    per-jid specific quotas. The value is a JSON object where key is a user bare jid and
    value is a quota.

  Quotas can be either ``null`` for unlimited space, or a size value (`SI prefixes and
  binary prefixes`_ can be used).

  example::

    quotas_json = {
      "admins": null,
      "users": "50 Mio",
      "jids": {"pierre@example.org": "1 Gio"}
    }

  .. _SI prefixes and binary prefixes: https://en.wikipedia.org/wiki/Octet_(computing)#Unit_multiples
