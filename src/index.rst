#########################################################
The Web Framework that scales with you and your agent
#########################################################

.. container:: quicklinks

   - `Start minimal <https://turbogears.readthedocs.io/en/latest/turbogears/minimal/index.html>`_
   - `Create an API server <https://github.com/TurboGears/tg2docs/blob/tg2.5.1/docs/turbogears/api.rst>`_
   - `Make webapps in minutes <https://turbogears.readthedocs.io/en/latest/turbogears/gearbox.html#quickstart>`_
   - `Work with your agents <https://github.com/TurboGears/tg2docs/blob/tg2.5.1/docs/turbogears/agent-tooling.rst>`_

TurboGears is a Python web framework for single-file services, JSON APIs
(application programming interfaces) and database-backed web applications.
Start with a small application; add controllers, templates, persistence and
authentication as your application's needs grow. Use Python 3.10 or newer in
a virtual environment. The API and agent links above open the 2.5.1
documentation on GitHub.

Start Small
===========

Save this minimal-mode application as ``myapp.py``. Its root controller
serves the home page; ``expose`` makes the method available over HTTP.

.. code-block:: python
   :emphasize-lines: 5-8

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

Install TurboGears and run it, then open http://localhost:8080/:

.. code-block:: bash

   python -m pip install TurboGears2
   python myapp.py

Grow to a Full-Stack Application
================================

When you need a structured project, ``tg.devtools`` provides Gearbox, the
command-line development toolkit. Its web application quickstart generates
controllers, templates, authentication and SQLAlchemy database models.
The setup command below intentionally initializes the development database,
including demo data; it is not a read-only check.

.. code-block:: bash

   python -m pip install tg.devtools
   gearbox quickstart myproj
   cd myproj
   python -m pip install -e '.[development]'
   gearbox setup-app -c development.ini
   gearbox serve -c development.ini

Open http://localhost:8080/ and follow the generated ``README.rst`` to replace
the demo with your application. For a JSON API instead, start with
``gearbox quickstart-api myapi`` and the GitHub API guide linked above.

Work with Your Agents
=====================

Coding assistants can use the quickstart's ``AGENTS.md`` project instructions
and optional skills (Markdown guidance for development). ``tginfo`` inspects
project structure, ``scaffold`` creates conventional project files, and
``tgshell`` runs checks in the application context. These tools help with
development; they are not AI features or dependencies of your running app.

From the installed project's root, inspect it or add skills to an existing
project:

.. code-block:: bash

   gearbox tginfo summary --project . --config development.ini --json
   gearbox tgskills

``tginfo`` is read-only, but importing application code can run startup side
effects. Read ``AGENTS.md``, review changes and run the project's tests;
only run database setup or migrations when you intend to change that database.

.. toctree::
   :hidden:

   /current-status
   /documentation
   /features
   /resources
