.. include:: /features/shallow-sidebar.rst

###############################
 WSGI: Tomorrow's Architecture
###############################

For many years, authors of Python web applications and pages had to rely on non-standard methods to get data from their code to the user's web browser. CGI, FastCGI, mod_python, and proprietary interfaces were all used with varying degrees of success.

The result was a chaotic mess. The situation became unbearable if you wanted to have multiple web applications being served in the same domain at the same time from the same web server.

Fortunately, WSGI was created. Using WSGI, we have a stable standard for hosting our Python web applications. As an added bonus, if we need to have multiple applications being served from the same web server to the same domain, we can do so.

In fact, it's not just possible, it's easy.

TurboGears takes full advantage of WSGI. We recommend using it for deploying your applications, and we provide ways to host WSGI applications inside of your own TurboGears based application.
