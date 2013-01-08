import os
import ldap
import turbogears
import logging 
import saprovider

class log:
    default=logging.getLogger('emailgency.system.saldapprovider')
    system=logging.getLogger('emailgency.system') 

class SaLdapIdentityProvider(saprovider.SqlAlchemyIdentityProvider):
    """
    IdentityProvider that uses LDAP for authentication.
    """
    def __init__(self):
        saprovider.SqlAlchemyIdentityProvider.__init__(self)
        get = turbogears.config.get
        self.host = get("identity.saldapprovider.host", "directory.example.COM")
        self.port = get("identity.saldapprovider.port", 389)
        self.basedn  = get("identity.saldapprovider.basedn", "o=example.com")
        self.autocreate = get("identity.saldapprovider.autocreate", True)
        log.default.info("host :: %s" % self.host)
        log.default.info("port :: %d" % self.port)
        log.default.info("basedn :: %s" % self.basedn)
        log.default.info("autocreate :: %s" % self.autocreate)

    def validate_identity( self, user_name, password, visit_key ):
        """
        Look up the identity represented by user_name and determine
        whether the password is correct.
        Must return either None if the credentials weren't valid or an
        object
        with the following properties:
            user_name: original user name
            user: a provider dependant object (TG_User or similar)
            groups: a set of group IDs
            permissions: a set of permission IDs
        """
        if not self.autocreate:
            return saprovider.SqlAlchemyIdentityProvider.validate_identity(user_name, password, visit_key )
#         user = user_class.query.filter_by(user_name=user_name).first()
#         if not user:
#             log.warning("No such user: %s", user_name)
#             return None
#         if not self.validate_password(user, user_name, password):
#             log.info("Passwords don't match for user: %s", user_name)
#             return None
#         log.info("Associating user (%s) with visit (%s)",
#             user_name, visit_key)
#         return SqlAlchemyIdentity(visit_key, user)

        user=None
        user=saprovider.user_class.query.filter_by(user_name=user_name).first()
        if not self.validate_password(user, user_name, password):
            log.default.info( "user '%s' or password invalid",user_name )
            return None
        if not user:
            try:
                user=saprovider.user_class(user_name=user_name,email_address=user_name, display_name=user_name, password=u'ldap')
            except:
                log.default.error( "Creating user: %s", user_name )
                return None
            else:
                log.default.info( "user created: %s", user_name )
                
        #         Skip the groups stuff we're not interested (Noufal)
        #         for gr in user.groups: user.removeGroup(gr)
        #         for gr_name in group_lst:
        #             user.addGroup(saprovider.group_class.by_group_name(gr_name))
        #         log.default.info( 'user "%s"in groups %r', user_name,group_lst )
        # Link the user to the visit
        #         link=saprovider.visit_class.query.filter_by(visit_key = visit_key)
        link=saprovider.visit_class.query.filter_by(visit_key = visit_key).first()
        if link:
            link.user_id = user.user_id
        else:
            link = saprovider.visit_class(visit_key=visit_key,user_id=user.user_id )
            saprovider.session.flush()
        return saprovider.SqlAlchemyIdentity( visit_key, user )
    
    def validate_password( self, user, user_name, password ):
        '''
        Validates user_name and password against an AD domain.
        
        '''
        ldapcon = ldap.open(self.host, self.port)
        filter = "(uid=%s)" % user_name
        rc = ldapcon.search(self.basedn, ldap.SCOPE_SUBTREE, filter)
        objects = ldapcon.result(rc)[1]
        if(len(objects) == 0):
            log.default.warning("No such LDAP user: %s" % user_name)
            return False
        elif(len(objects) > 1):
            log.default.error("Too many users: %s" % user_name)
            return False
        dn = objects[0][0]
        try:
            rc = ldapcon.simple_bind(dn, password)
            ldapcon.result(rc)
        except ldap.INVALID_CREDENTIALS:
            log.default.error("Invalid password supplied for %s" % user_name)
            return False
	return True
