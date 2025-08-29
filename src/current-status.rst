########################
Project Status
########################

Latest stable release: 2.5.0 — released February 18, 2025

Release announcement available at: https://github.com/TurboGears/tg2/releases/tag/tg2.5.0

***************************
Contributing to TurboGears
***************************

All the TurboGears related projects are available on GitHub under the `TurboGears`_ account,
if you want to take a look at TurboGears source code you can start there.
In particular, we have several repositories for public use. The main ones are:

- `TG2.x Core (Git)`_ - The actual framework code lives here
- `TG2.x Devtools (Git)`_ - Useful tools used during development
- `TG2.x Docs (Git)`_ - The documentation repository

For continuous integration work, we use `Travis`_.

**JetBrains** has been supporting the TurboGears development team with `PyCharm`_ licenses,
which has been the development environment of choice for some of TurboGears contributors.

Development happens on two core branches: the ``development`` one where major changes for
the upcoming scheduled release happens and ``master`` branch which will point to the
current stable release. Minor bugfix releases are branched from master on demand and merge
back into the master branch when the release happens.

To create your development environment you can perform:

.. code-block:: bash

   virtualenv ${HOME}/tg2env
   source ${HOME}/tg2env/bin/activate
   git clone git@github.com:TurboGears/tg2.git
   cd tg2
   git checkout development
   pip install -e .[testing]

.. _`TG2.x Core (Git)`: https://github.com/TurboGears/tg2
.. _`TG2.x Devtools (Git)`: https://github.com/TurboGears/tg2devtools
.. _`TG2.x Docs (Git)`: https://github.com/TurboGears/tg2docs
.. _`Travis`: https://travis-ci.org/TurboGears/tg2
.. _`TurboGears`: https://github.com/TurboGears
.. _`PyCharm`: http://www.jetbrains.com/pycharm/
