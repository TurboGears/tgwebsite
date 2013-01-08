#--
# Cookie default
# This is a decorator you can use around a TurboGears controller method, like
# this:
#
#   @expose()
#   @cookie_default(name='', location='Head Office', filter='')
#   def lookup(self, name, location, filter):
#       ...
#--
import turbogears as tg, cherrypy as cp

def cookie_default(*default_groups, **kw):
    cookie_name = kw.get('cookie_name', 'default')
    def entangle(func):
        def inner(func, *args, **kw):

            #--
            # Decode the cookie. Ignore all errors in decoding - this avoids a
            # user being locked out of the app if their cookie becomes invalid
            # for some reason.
            #--
            cdata = {}
            cookie = ''
            try:
                cookie = cp.request.simple_cookie[cookie_name].value
                cdata = dict(v.split('#') for v in cookie.split('$'))
                for k in cdata:
                    cdata[k] = cdata[k].decode('base64').decode('utf-8')
            except Exception, e:
                print "Error decoding cookie: %s" % repr(cookie)
                pass              
            
            #--
            # Go through each default group. If any parameters are specified in QS
            # or POST, use the values and blank others. Otherwise use cookie if
            # present, or hard-coded defaults as last resort.
            #--
            generate_cookie = False
            for dg in default_groups:
                if [1 for k in dg if kw.has_key(k)]:
                    generate_cookie = True
                    for k in dg:
                        kw.setdefault(k, '')                                    
                else:
                    if cdata:
                        for k in dg:                            
                            kw[k] = cdata.get(k)
                    else:
                        kw.update(dg)

            #--
            # Generate a new cookie
            #--
            if generate_cookie:
                cdata = {}
                for d in default_groups:
                    cdata.update(dict((k,kw[k]) for k in d))
                for k,v in cdata.iteritems():
                    if not isinstance(v, basestring):
                        cdata[k] = unicode(v)
                    cdata[k] = v.encode('utf-8').encode('base64').strip()
                cookie = '$'.join(['%s#%s' % v for v in cdata.iteritems()])
                cp.response.simple_cookie[cookie_name] = cookie
                cp.response.simple_cookie[cookie_name]['path'] = '/'
                cp.response.simple_cookie[cookie_name]['max-age'] = '31536000'

            return func(*args, **kw)
        return inner
    return tg.decorator.weak_signature_decorator(entangle)
