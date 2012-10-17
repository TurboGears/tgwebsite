.. include:: /features/shallow-sidebar.rst

#######
 Reuse
#######

TurboGears tries to give you the power to reuse the component that you already know instead of forcing you to learn a new one. We accomplish this in three ways.

First, we support the best toolkits out of the box: Genshi, Mako, SQLAlchemy, ToscaWidgets, all of these work without your having to do any extra code.

Second, we provide methods for you to add your preferred toolkit right into the stack at various places. Thanks to this, people have added support for Jinja2, FastPT, and others.

Third, we use WSGI. With WSGI, you can mount your own application inside of a TurboGears application, and vice versa. While the coupling between the TurboGears application and the other might not be as tight as desired (for instance, authentication could be totally different), it is at least possible to extend and reuse your existing code in the ways you want to use it.

Thanks to all of this, the code that you already have and use for other projects is easily incorporated into your new TurboGears application. The possibilities are endless.
