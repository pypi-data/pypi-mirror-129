.. image:: https://img.shields.io/pypi/l/Clor.svg
   :target: https://spdx.org/licenses/LGPL-2.1+.html
   :alt: PyPI - License
.. image:: https://heptapod.host/saajns/clor/badges/branch/default/pipeline.svg
   :target: https://heptapod.host/saajns/clor/-/commits/branch/default
   :alt: Pipeline status
.. image:: https://heptapod.host/saajns/clor/badges/branch/default/coverage.svg
   :target: https://heptapod.host/saajns/clor/-/commits/branch/default
   :alt: Test code coverage
.. image:: https://badge.fury.io/py/Clor.svg
   :target: https://pypi.org/project/Clor/
   :alt: PyPI

====
Clor
====
Clor is a tiny wrapper around ``logging`` configuration system [1]_, which allows
its reuse for general application configuration. The name was coined this way:
"configurator" → "c10r" → "clor".

Usage
=====
Normally there's a configuration module (e.g. ``envconf.py``), or a YAML file. Here
is a CherryPy example:

.. code:: python

   base = {
     'global' : {
       'server.socket_host' : '127.0.0.1',
       'server.socket_port' : 8080,
       'server.thread_pool' : 8
     },
     'app' : {
       'api' : {
         '/' : {
           'request.dispatch' : {
             '()' : 'cherrypy._cpdispatch.MethodDispatcher'
           }
         }
       }
     }
   }

   production = (base, {
     'global' : {
       'server.socket_host' : '0.0.0.0',
       'server.thread_pool' : 16,
       'tools.auth_basic.on'            : True,
       'tools.auth_basic.realm'         : 'App',
       'tools.auth_basic.checkpassword' : 'ext://someapp.password.checker'
     },
   })

   development = (base, {
     'global' : {
       'server.thread_pool' : None,
     },
     'app' : {
       'api' : {
         '/' : {
           'tools.response_headers.on'      : True,
           'tools.response_headers.headers' : [('Access-Control-Allow-Origin', '*')]
         }
       },
       'api2' : 'cfg://app.api'
     }
   })

A few observations:

* Nest dictionaries are merged recursively
* ``logging``'s ``ext`` pseudo-protocols
* ``logging``'s ``cfg`` pseudo-protocols
* ``logging``'s instantiation with ``()`` key
* Keys having ``None`` value are removed

Then in your bootstrapping code you can do:

.. code:: python

   import clor

   from . import envconf


   config = clor.configure(*getattr(envconf, 'production'))

   cherrypy.config.update(config)
   cherrypy.tree.mount(ApiApplication(), '/api', config['app']['api'])


.. [1] https://docs.python.org/3/library/logging.config.html
