Resources and Community

For the TurboGears project, we use a great many resources that are available to the community.

Community Projects and Extensions

For community made projects related to TurboGears take a look at the CogBin, to have your project listed there just put it on PyPi and provide the right keywords.

Project Status

We have moved TurboGears 2 over to Github. TurboGears 1 will, for the foreseeable future, remain on Sourceforge. All main development is happening on Github, so please track the goings on there. 

Mailing Lists and IRC

For our mailing lists, we use Google Groups, both for the development and end user lists.

Finally, we also have an irc channel.

As you can see, we're on a lot of places. We hope to see you on one of them!

How To Contribute

For source code management and issue tracking, we use Github. In particular, we have several repositories for public use. The main ones are:

TG2.x Core (Git) - The actual framework code lives here
TG2.x Devtools (Git) - Useful tools used during development
TG2.x Docs (Git) - The documentation repository
For continuous integration work, we use Jenkins.

As you can see, we are sharing this instance with other projects, but we still get quite a bit of good work out of it.

To create your development environment you can perform:

virtualenv --no-site-packages ${HOME}/tg2env
source ${HOME}/tg2env/bin/activate
git clone git@github.com:TurboGears/tg2.git
cd tg2
python setup.py tgdevelop
python setup.py tgtesting
python setup.py tgnose
 For contributing to TG1 the available resources are:

 

TG1 Issues - The Sourceforge Issue Tracker for TG1
TG1 (SVN) - All TurboGears1 code lives here
How do I provide translations for the site?

The site is managed by a CMS known as tgext.pages. There are no .po or .pot files to manage or update. Instead, if you wish to provide a translation to your language for any given page, you need to send an email to our Google Group mailing list with the following information:

The URL of the page you are translating
The two character language code of the language you are translating to
The title of the page in that language
The name that will appear in the menu bar in that language
The text of that page in that language.
For instance, to translate the welcome page to French, you would send an email looking like the following:

Subject: Translation of welcome page
URL: http://beta.turbogears.org/en/welcome
Title: Bienvenue
Menu Name: Bienvenue
Page Text:
Bienvenue sur notre site. Ce site est le site de TurboGears.

And we would then upload the translation for that page.
