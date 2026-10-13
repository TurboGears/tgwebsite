.. include:: features/shallow-sidebar.rst

########
Features
########

TurboGears gives you the power and structure to build anything from a concise
single-file web service up to high-traffic, multi-database enterprise applications.
It scales with you and your development workflows.

Intuitive Web Controllers & Object Dispatch
===========================================

* **Natural as writing a function**: Expose Python methods as endpoints with simple decorators like ``@expose()``.
* **Object Dispatch**: Map URLs directly to nested controller trees with explicit routing hierarchy, plus dynamic dispatch via ``_lookup`` and ``_default``.
* **Clean REST dispatch**: Dedicated ``tg.RestController`` mapping HTTP verbs (``get_one``, ``get_all``, ``post``, ``put``, ``delete``) to standard RESTful resource actions.
* **Pluggable template engines**: Built-in support for Kajiki XML templates, Jinja2, Genshi, and Mako, with automatic context passing and format switching.

Full API Server Capabilities & OpenAPI
======================================

* **Dedicated API quickstart**: Spin up production-grade JSON API servers in seconds with ``gearbox quickstart-api``.
* **Automatic OpenAPI specs**: Built-in ``tgext.apispec`` integration automatically generates OpenAPI 3.0 / Swagger specifications from controller annotations and schemas.
* **Interactive API documentation**: Zero-maintenance interactive Redoc documentation mounted out of the box at ``/api/docs``.
* **Automatic parameter validation**: Declarative request parameter schema validation with ``@validate``, returning standard JSON 422 error structures on invalid payloads.
* **Automatic JSON request decoding**: Native JSON request body handling alongside traditional form encoding.

Multi-Database Persistence & Migrations
=======================================

* **First-class SQLAlchemy 2.0**: The industry standard ORM out of the box with unit-of-work sessions and transaction management.
* **Multi-database & horizontal sharding**: Native support for connecting to multiple databases, master-slave replicas, and horizontal data partitioning within the same application.
* **MongoDB support**: Full NoSQL integration via Ming for document-oriented storage.
* **Automated database migrations**: Integrated Alembic and SQLAlchemy-Migrate toolchain via ``gearbox migrate`` with schema autogeneration and versioning.

Security, Auth & Enterprise Ready
=================================

* **Dual authentication out of the box**: First-class support for both API Bearer tokens and web session cookies with CSRF protection.
* **Granular authorization**: Rich predicate-based permission system supporting users, groups, and permissions with clear declarative checks.
* **Pluggable identity backends**: Pluggable authentication backends via ``repoze.who`` for LDAP, OAuth, OAuth2, and custom authenticators.
* **Session & caching**: Flexible web session storage (JSON-serialized, secure cookies, Redis, Memcached) and multi-backend caching.
* **Internationalization**: Full gettext-based translation and localization pipeline driven by ``gearbox i18n``.

Agentic Development & Project-Aware Tooling
===========================================

* **AI Coding Agent Skills**: Ready-to-use agent skills (``tg-inspect``, ``tg-scaffold``, ``tg-shell``) adhering to the Agent Skills standard, supporting Pi, Claude Code, and other coding harnesses.
* **Structured project inspection**: ``gearbox tginfo`` provides read-only JSON introspections of routes, controllers, models, templates, and available scaffolds so coding assistants never have to guess project layout.
* **Smart scaffolding**: ``gearbox scaffold`` creates conventional controllers, models, templates, and functional tests in one pass.
* **Application-aware shell**: ``gearbox tgshell`` provides interactive and scriptable inspection of fully loaded apps with in-memory WebTest request execution.
* **Automated onboarding**: Quickstarts generate project-local ``AGENTS.md`` providing coding agents with architectural conventions, test commands, and safe execution boundaries.

Extensibility & Pluggable Architecture
======================================

* **Pluggable Applications**: Mount complete reusable modular applications with their own controllers, models, templates, and static assets inside host projects.
* **Standard WSGI compatibility**: Mount external WSGI applications or deploy TurboGears behind any WSGI or ASGI server.
* **The CogBin ecosystem**: Rich catalog of community-contributed extensions, widgets, and pluggable applications available on PyPI.
