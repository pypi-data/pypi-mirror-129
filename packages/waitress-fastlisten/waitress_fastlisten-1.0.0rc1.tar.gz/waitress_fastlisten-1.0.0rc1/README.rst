==============================================
A fast listen implementation for Waitress WSGI
==============================================

This tiny package allows the waitress WSGI server to immediatly pre-bind to a port and listen to it.
It waits then for the app to start up and passes then requests further.


Usage
=====

In your paste based WSGI configuration in ``[server:main]`` set:

- ``paste-server-factory`` to ``waitress_fastlisten:main``
- ``use`` to ``egg:plone.recipe.zope2instance#main``
- ``fast-listen`` to ``HOST:PORT``

Do *not* set "listen =".

Example:

.. code-block:: INI

    [server:main]
    paste.server_factory = plone.recipe.zope2instance:main
    use = egg:plone.recipe.zope2instance#main
    fast-listen = 0.0.0.0:8080
