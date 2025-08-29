.. _cogbintop:

############
 The Cogbin
############

When you quickstart a TurboGears project, the setup.py file already contains the metadata you need. It's just commented out. Choose the right keywords for the kind of project you're releasing, and you're all set.

TurboGears packages added to the `Python Package Index`_ will automatically appear in the CogBin!

The table below has the keywords you should use as well:

.. note::
   To have your package discovered and listed here, declare one of the
   following keywords in your package metadata on PyPI:

   - ``turbogears2`` (general)
   - ``turbogears2.application``
   - ``turbogears2.extension``
   - ``turbogears2.widgets``
   - ``turbogears2.command``

   Examples:

   - ``pyproject.toml``: add under ``[project]`` → ``keywords = ["turbogears2.extension"]``
   - ``setup.cfg``: add under ``[metadata]`` → ``keywords = turbogears2.extension``
   - ``setup.py``: ``setup(keywords=["turbogears2.extension"])``

.. cogbin::
    

.. _`Python Package Index`: http://pypi.python.org/
