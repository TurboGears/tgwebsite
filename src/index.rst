##########################
 TurboGears Web Framework
##########################

.. include:: welcome/sidebar.rst
   
*********************************************************
 The next generation web framework that scales with you.
*********************************************************

TurboGears will help you to create a database-driven, ready-to-extend application in minutes. All with code that is `as natural as writing a function`_, `designer friendly templates`_, easy `AJAX`_ on the `browser side`_ and on the `server side`_ and with an incredibly powerful and flexible `Object Relational Mapper (ORM)`_.

***************
 Give It a Try
***************

.. code-block:: bash

   $ virtualenv --no-site-packages tg2env
   $ cd tg2env/
   $ source bin/activate
   (tg2env)$ easy_install -i http://tg.gy/current tg.devtools
   (tg2env)$ paster quickstart example
   (tg2env)$ cd example
   (tg2env)$ python setup.py develop -i http://tg.gy/current
   (tg2env)$ paster setup-app development.ini
   (tg2env)$ paster serve development.ini

Get started Learning TurboGears 2 by looking at our famous `wiki tutorial`_.

Follow on `Google+`_ for the latest news.

############################################
 A new Generation in dynamic web frameworks
############################################


TurboGears 2 is built on top of the experience of several next generation web frameworks including TurboGears 1 (of course), Django, and Rails. All of these frameworks had limitations that frustrated us, and TG2 was built as an answer to that frustration. We wanted something that had:

* Real multi-database support
* Support for Horizontal data partitioning (aka, sharding)
* Support for a variety of JavaScript toolkits, and new widget system to make building ajax heavy apps easier
* Support for multiple data-exchange formats
* Built in extensibility via standard WSGI components
* Programmer friendly template system that also works for designers

.. _`Overview`: welcome/overview.html
.. _`Presentations`: welcome/presentations.html
.. _`The TurboGears Way`: welcome/turbogears-way.html
.. _`as natural as writing a function`: http://www.turbogears.org/2.1/docs/main/Controllers.html
.. _`designer friendly templates`: http://genshi.edgewall.org/
.. _`AJAX`: http://en.wikipedia.org/wiki/AJAX
.. _`browser side`: http://www.toscawidgets.org/
.. _`server side`: http://www.pylonshq.org/
.. _`Object Relational Mapper (ORM)`: http://www.sqlalchemy.org/
.. _`wiki tutorial`: http://www.turbogears.org/book/part1/wiki20.html
.. _`Google+`: https://plus.google.com/115723575598932631951


.. toctree::
   :hidden:
   
   /index
   /current-status
   /documentation
   /features
   /resources
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
