.. include:: welcome/sidebar.rst

#######################################
The Web Framework that scales with you.
#######################################

TurboGears 2 is built on top of the experience of several next generation web frameworks including TurboGears 1 (of course), Django, and Rails.
All of these frameworks had limitations that frustrated us, and TG2 was built as an answer to that frustration:

Start Small
===========

TurboGears can start as a single file app through its `minimal mode`_ setup:

.. code-block:: python
   :emphasize-lines: 6-9

    from wsgiref.simple_server import make_server
    from tg import MinimalApplicationConfigurator
    from tg import expose, TGController

    # RootController of our web app, in charge of serving content for /
    class RootController(TGController):
        @expose(content_type="text/plain")
        def index(self):
            return 'Hello World'

    # Configure a new minimal application with our root controller.
    config = MinimalApplicationConfigurator()
    config.update_blueprint({
        'root_controller': RootController()
    })

    # Serve the newly configured web application.
    print("Serving on port 8080...")
    httpd = make_server('', 8080, config.make_wsgi_app())
    httpd.serve_forever()

which you can then run on Python itself:

.. code-block:: bash

   $ pip install TurboGears2
   $ python myapp.py

Or Scale to a FullStack Solution
================================

TurboGears can scale to a `full stack solution`_ for more complex
applications using TurboGears `devtools`:

.. code-block:: bash

   $ pip install --pre tg.devtools
   $ gearbox quickstart myproj

The newly created `myproj` application can be started with the **Gearbox** toolchain:

.. code-block:: bash

   $ cd myproj
   $ pip install -e .
   $ gearbox serve

#############################
Feature Complete and Flexible
#############################


* Starts as a `microframework`_ and scales up to a `fullstack`_ solution
* Code that is `as natural as writing a function`_
* A powerful and flexible `Object Relational Mapper (ORM)`_ with real `multi-database support`_
* Support for Horizontal data partitioning (aka, sharding)
* A new `widget system`_ to make building `AJAX`_ heavy apps easier
* Support for multiple data-exchange formats
* Built in extensibility `Pluggable Applications`_ and standard WSGI components
* `Designer friendly template system`_ great for programmers

.. raw:: html

   <iframe src="http://ghbtns.com/github-btn.html?user=TurboGears&repo=tg2&type=watch&count=true&size=large"  width="140" height="35" style="display:inline;vertical-align:middle;margin-top:8px;border: none"></iframe>

.. rst-class:: inline

   or follow TurboGears on `Twitter`_ for the latest news!

Give It a Try
=============

TurboGears 2 works on Python 2.7, 3.4, 3.5, 3.6 and 3.7.

Or set it up in a `virtual environment`_ on your machine:

.. code-block:: bash

   $ virtualenv --no-site-packages tg2env
   $ cd tg2env/
   $ source bin/activate
   (tg2env)$ pip install tg.devtools

   (tg2env)$ gearbox quickstart example
   (tg2env)$ cd example/
   (tg2env)$ pip install -e .
   (tg2env)$ gearbox serve

Get started Learning TurboGears 2 by looking at `Documentation`_ and our famous `wiki tutorial`_.

.. _`minimal mode`: http://turbogears.readthedocs.io/en/latest/turbogears/minimal/index.html
.. _`full stack solution`: http://turbogears.readthedocs.io/en/latest/turbogears/wiki20.html
.. _`virtual environment`: https://virtualenv.pypa.io/en/stable/
.. _`Overview`: welcome/overview.html
.. _`Presentations`: welcome/presentations.html
.. _`The TurboGears Way`: welcome/turbogears-way.html
.. _`Documentation`: http://turbogears.readthedocs.io/en/latest/
.. _`microframework`: http://turbogears.readthedocs.io/en/latest/index.html#single-file-application
.. _`fullstack`: http://turbogears.readthedocs.io/en/latest/index.html#full-stack-projects
.. _`as natural as writing a function`: http://turbogears.readthedocs.io/en/latest/turbogears/wiki20.html#controller-code
.. _`Designer friendly template system`: http://genshi.edgewall.org/
.. _`AJAX`: http://en.wikipedia.org/wiki/AJAX
.. _`Pluggable Applications`: http://turbogears.readthedocs.io/en/latest/turbogears/Pluggable/index.html
.. _`widget system`: http://www.toscawidgets.org/
.. _`multi-database support`: http://turbogears.readthedocs.io/en/latest/cookbook/master-slave.html
.. _`Object Relational Mapper (ORM)`: http://www.sqlalchemy.org/
.. _`wiki tutorial`: http://turbogears.readthedocs.io/en/latest/turbogears/wiki20.html
.. _`Twitter`: https://twitter.com/turbogearsorg
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
