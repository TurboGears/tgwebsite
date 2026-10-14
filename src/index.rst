#################################
Start small. Build the whole app.
#################################

.. container:: home-intro

   TurboGears is a **Python web framework** for services, JSON APIs and
   database-backed web apps. Start with one file and grow into a full-stack
   project.

   .. container:: home-actions

      `Try TurboGears <#start-small>`_
      `Explore the docs <documentation.html>`_

.. container:: home-benefits

   .. container:: home-benefit

      **Start with one file**

      Serve your first response without a generated project. Add controllers
      and templates as you need them.

   .. container:: home-benefit

      **Build beyond the endpoint**

      Generate a web app with templates, SQLAlchemy models and authentication
      already connected.

   .. container:: home-benefit

      **Make your API discoverable**

      The API quickstart includes validation and generated OpenAPI
      documentation. `Build a JSON API → <https://turbogears.readthedocs.io/en/latest/turbogears/api.html>`_

.. rst-class:: home-start

Start small
===========

**One file. A working web service.**
Use Python 3.10+ in a virtual environment. Save this as ``myapp.py``:

.. code-block:: python

   from wsgiref.simple_server import make_server
   from tg import MinimalApplicationConfigurator
   from tg import expose, TGController

   class RootController(TGController):
       @expose(content_type="text/plain")
       def index(self):
           return 'Hello World'

   config = MinimalApplicationConfigurator()
   config.update_blueprint({
       'root_controller': RootController()
   })

   print("Serving on port 8080...")
   httpd = make_server('', 8080, config.make_wsgi_app())
   httpd.serve_forever()

Install and run:

.. code-block:: bash

   python -m pip install TurboGears2
   python myapp.py

Open http://localhost:8080/ to see **Hello World**.
`Keep building: the minimal tutorial → <https://turbogears.readthedocs.io/en/latest/turbogears/minimal/index.html>`_

.. rst-class:: home-full

Build the whole app
===================

**Ready for a database-backed project?**
Gearbox, the development toolkit, generates your application's structure.
In a Python 3.10+ virtual environment, run:

.. code-block:: bash

   python -m pip install tg.devtools
   gearbox quickstart myproj
   cd myproj
   python -m pip install -e '.[development]'
   gearbox setup-app -c development.ini
   gearbox serve -c development.ini

``setup-app`` creates a local development database with demo data.
Open http://localhost:8080/ to explore the generated app, then follow
its ``README.rst`` to make it your own.

`Full-stack quickstart guide → <https://turbogears.readthedocs.io/en/latest/turbogears/gearbox.html#quickstart>`_

Prefer an API? Use ``gearbox quickstart-api myapi`` and follow the
`JSON API tutorial <https://turbogears.readthedocs.io/en/latest/turbogears/api.html>`_.

.. rst-class:: home-agents

Give your coding agent project context
======================================

Generated project instructions and optional development tools help agents
inspect your app, create conventional project files and check it in a
running application context. Your app's runtime stays independent of
agent tooling.

`Explore agent tooling → <https://turbogears.readthedocs.io/en/latest/turbogears/agent-tooling.html>`_
· `See a worked example <https://turbogears.readthedocs.io/en/latest/turbogears/agentic-development.html>`_

.. toctree::
   :hidden:

   /current-status
   /documentation
   /features
   /resources
   /cogbin
