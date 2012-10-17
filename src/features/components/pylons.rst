.. include:: /features/deep-sidebar.rst

##################################
 Pylons, a WSGI to Object wrapper
##################################

Pylons brings much of the power of Ruby on Rails to the Python world. Routes and WebHelpers are both Python re-implementations of the same features in the RoR world.

Pylons does not stop at just being a RoR re-implementation, though. It provides an architecture, built around WSGI, that allows the developer to plug in their favorite components (templating languages, database engines, widget toolkits, and more).

The result is a strong system, kept lean at its core, that allows the developer to choose the way in which the application grows.

Even though this is great, it does make for some issues: Should I choose Genshi, or Mako, or some other templating engine? How do I connect to the database? How do I handle turning URLs into function calls?

TurboGears answers all of these questions by providing a fully configured stack out of the box. Instead of you, the developer, having to research what will suit your needs best, we have done the work to find the best of breed for all of these choices already. We configure a full WSGI middleware stack in a single command, allowing you to get to work on your application quickly.

Pylons provides the foundation. We build on top of that, to provide the framework. What you do with it from there is limited only by your imagination.
