"""
This plugin provides authentication of passwords against UNIX password files (and NIS implicitly).

Installation Instructions:

1.) Copy this file to: <TURBOGEARS_INSTALL_DIR>/turbogears/identity/
2.) Add the plugin to the TurboGears entry points file: <TURBOGEARS_INSTALL_DIR>/EGG-INFO/entry_points.txt
    Under the [turbogears.identity.provider] section, add the following line:
    sqlpwd = turbogears.identity.sopwdprovider:SoPwdIdentityProvider
3.) Inside the site's app.cfg, change the identity.provider setting to:
    identity.provider='sqlpwd'
    
"""

from crypt import crypt
import pwd

from soprovider import * 

class SoPwdIdentityProvider(SqlObjectIdentityProvider):
    """
    IdentityProvider that uses UNIX password files (or NIS implicitly)
    """

    def validate_password(self, user, user_name, password):
        '''
        Validates user_name and password against UNIX password. 
        '''
        log.debug("Validating User '%s' against PWD database" % user_name)

        try:
            # Get the DES encrypted password from the password database
            crypted_password = pwd.getpwnam(user_name)[1]
        except KeyError, e:
            log.error("User '%s' not found in PWD database" % user_name)
            return False

        # Encrypt the password trial using DES with the correct password as the salt
        auth_password = crypt(password, crypted_password[:2])

        # Make sure the encrypted passwords match
        return crypted_password == auth_password
