.. include:: welcome/sidebar.rst

############################################################
The Web Framework that scales with you.
############################################################

TurboGears 2 is built on top of the experience of several next generation web frameworks including TurboGears 1 (of course), Django, and Rails.
All of these frameworks had limitations that frustrated us, and TG2 was built as an answer to that frustration:

* Starts as a `microframework`_ and scales up to a `fullstack`_ solution
* Code that is `as natural as writing a function`_
* A powerful and flexible `Object Relational Mapper (ORM)`_ with real `multi-database support`_
* Support for Horizontal data partitioning (aka, sharding)
* A new `widget system`_ to make building `AJAX`_ heavy apps easier
* Support for multiple data-exchange formats
* Built in extensibility `Pluggable Applications`_ and standard WSGI components
* `Designer friendly template system`_ great for programmers

.. rst-class:: googleplus

Follow TurboGears on `Google+`_ for the latest news!

***************
 Give It a Try
***************

| TurboGears 2 works on Python 2.6, 2.7, 3.2, 3.3 and 3.4.
| Try it now, in your browser, using `Runnable`_

Or set it up on your machine:

.. code-block:: bash

   $ virtualenv --no-site-packages tg2env
   $ cd tg2env/
   $ source bin/activate
   (tg2env)$ pip install tg.devtools

Start a single file Hello World

.. code-block:: python

    from wsgiref.simple_server import make_server
    from tg import expose, TGController, AppConfig

    class RootController(TGController):
         @expose()
         def index(self):
             return "<h1>Hello World</h1>"

    config = AppConfig(minimal=True, root_controller=RootController())

    print "Serving on port 8080..."
    httpd = make_server('', 8080, config.make_wsgi_app())
    httpd.serve_forever()

Or with a Full Stack project:

.. code-block:: bash

   (tg2env)$ gearbox quickstart example
   (tg2env)$ cd example/
   (tg2env)$ python setup.py develop
   (tg2env)$ gearbox serve

Get started Learning TurboGears 2 by looking at `Documentation`_ and our famous `wiki tutorial`_.

.. _`Overview`: welcome/overview.html
.. _`Presentations`: welcome/presentations.html
.. _`The TurboGears Way`: welcome/turbogears-way.html
.. _`Documentation`: http://turbogears.readthedocs.org/en/latest/
.. _`microframework`: http://turbogears.readthedocs.org/en/latest/index.html#single-file-application
.. _`fullstack`: http://turbogears.readthedocs.org/en/latest/index.html#full-stack-projects
.. _`as natural as writing a function`: http://turbogears.readthedocs.org/en/latest/turbogears/wiki20.html#controller-code
.. _`Designer friendly template system`: http://genshi.edgewall.org/
.. _`AJAX`: http://en.wikipedia.org/wiki/AJAX
.. _`Pluggable Applications`: http://turbogears.readthedocs.org/en/latest/turbogears/Pluggable/index.html
.. _`widget system`: http://www.toscawidgets.org/
.. _`multi-database support`: http://turbogears.readthedocs.org/en/latest/cookbook/master-slave.html
.. _`Object Relational Mapper (ORM)`: http://www.sqlalchemy.org/
.. _`wiki tutorial`: http://turbogears.readthedocs.org/en/latest/turbogears/wiki20.html
.. _`Google+`: https://plus.google.com/115723575598932631951
.. _`Runnable`: http://runnable.com/Unq2c2CaTc52AAAm/basic-turbogears-example-for-python

.. toctree::
   :hidden:
   
   /index
   /current-status
   /documentation
   /features
   /resources
   /cogbin
   /welcome/overview
   /welcome/presentations
   /welcome/turbogears-way
   /whos-using
   /features/components
   /features/deep-sidebar
   /features/reuse
   /features/shallow-sidebar
   /features/wsgi
   /features/components/genshi
   /features/components/mako
   /features/components/pylons
   /features/components/sqlalchemy
