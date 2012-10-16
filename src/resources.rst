#########################
 Resources and Community
#########################

For the TurboGears project, we use a great many resources that are available to the community.

***********************************
 Community Projects and Extensions
***********************************

For community made projects related to TurboGears take a look at the `CogBin`_, to have your project listed there just put it on PyPi and provide the right keywords.

****************
 Project Status
****************

We have moved `TurboGears 2`_ over to `Github`_. `TurboGears 1`_ will, for the foreseeable future, remain on `Sourceforge`_. All main development is happening on `Github`_, so please track the goings on there. 

***********************
 Mailing Lists and IRC
***********************

For our mailing lists, we use Google Groups, both for the `development`_ and `end user`_ lists.

Finally, we also have an `irc channel`_.

As you can see, we're on a lot of places. We hope to see you on one of them!

*******************
 How To Contribute
*******************

For source code management and issue tracking, we use Github. In particular, we have several repositories for public use. The main ones are:

- `TG2.x Core (Git)`_ - The actual framework code lives here
- `TG2.x Devtools (Git)`_ - Useful tools used during development
- `TG2.x Docs (Git)`_ - The documentation repository

For continuous integration work, we use `Jenkins`_.

As you can see, we are sharing this instance with other projects, but we still get quite a bit of good work out of it.

To create your development environment you can perform:

.. code-block:: bash

   virtualenv --no-site-packages ${HOME}/tg2env
   source ${HOME}/tg2env/bin/activate
   git clone git@github.com:TurboGears/tg2.git
   cd tg2
   python setup.py tgdevelop
   python setup.py tgtesting
   python setup.py tgnose

For contributing to TG1 the available resources are: 

- `TG1 Issues`_ - The Sourceforge Issue Tracker for TG1
- `TG1 (SVN)`_ - All TurboGears1 code lives here

*********************************************
 How do I provide translations for the site?
*********************************************

The site is managed by a CMS known as tgext.pages. There are no .po or .pot files to manage or update. Instead, if you wish to provide a translation to your language for any given page, you need to send an email to our Google Group mailing list with the following information:

- The URL of the page you are translating
- The two character language code of the language you are translating to
- The title of the page in that language
- The name that will appear in the menu bar in that language
- The text of that page in that language.

For instance, to translate the welcome page to French, you would send an email looking like the following::

  Subject: Translation of welcome page
  URL: http://beta.turbogears.org/en/welcome
  Title: Bienvenue
  Menu Name: Bienvenue
  Page Text:
  Bienvenue sur notre site. Ce site est le site de TurboGears.

And we would then upload the translation for that page.

.. _`CogBin`:  http://turbogears.org/cogbin
.. _`TurboGears 2`: https://www.github.com/TurboGears/
.. _`Github`: https://www.github.com/
.. _`TurboGears 1`: https://sourceforge.net/p/turbogears2/turbogears1/
.. _`Sourceforge`: https://www.sf.net/
.. _`development`: http://groups.google.com/group/turbogears-trunk
.. _`end user`: http://groups.google.com/group/turbogears
.. _`irc channel`: irc://irc.freenode.net/turbogears
.. _`TG2.x Core (Git)`: https://github.com/TurboGears/tg2
.. _`TG2.x Devtools (Git)`: https://github.com/TurboGears/tg2devtools
.. _`TG2.x Docs (Git)`: https://github.com/TurboGears/tg2docs
.. _`Jenkins`: http://jenkins.turbogears.org/view/TurboGears%20Hosted/
.. _`TG1 Issues`: http://sourceforge.net/p/turbogears1/tickets/
.. _`TG1 (SVN)`: http://sourceforge.net/p/turbogears1/code/
