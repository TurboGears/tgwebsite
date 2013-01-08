# sosmbprovider.py
"""
NOTE: This is intended as "example code", not as a finished product!
Use at your own risk. (etc.)

Written by Joel Pearson for the TurboGears project.

This is a TurboGears Identity provider that's identical to the SQLObject
provider, except that passwords are checked against a Windows/Samba domain. 
To be more precise, it's a subclass of SqlObjectIdentityProvider that
overrides the validate_password() method.

IMPORTANT: This is *not* a standalone SMB Identity provider!
You still have to create a user record in the database for each
domain user that you want to have log in. The only difference between this 
provider and the standard sqlobject provider is that sosmbprovider ignores 
the password field in the user model, and validates the user-supplied password
against the domain password, instead.

It requires Python Win32 extensions, so it only works on Windows servers.

To use:

1) IMPORTANT: Follow all instructions provided for setting up and using the 
SqlObjectProvider, including creating the tables and adding users and groups. 
Try logging in. MAKE SURE THIS WORKS BEFORE PROCEEDING! None of what follows
will work until the standard "sqlobject" provider is working.

2) Install the Win32 extensions.

3) Save this file into the identity folder under your TurboGears installation
as "sosmbprovider.py".

4) Edit the entry_points.txt file of your TurboGears installation (such as
C:\Python24\Lib\site-packages\TurboGears-0.9a6-py2.4.egg\EGG-INFO\entry_points.txt)
and add the following line under the [turbogears.identity.provider] section:

sosmbprovider = turbogears.identity.sosmbprovider:SoSmbIdentityProvider

5) Add the following lines under the [global] section in a config file (such as app.cfg):

identity.provider='sosmbprovider'
identity.sosmbprovider.smb_domain="PUT_YOUR_DOMAIN_HERE"

6) Restart TurboGears, and try to log in. Identity should authenticate logins
using the usernames and passwords of the domain you specified in step 4.

"""

from soprovider import *

from win32security import LogonUser, LOGON32_LOGON_NETWORK, LOGON32_PROVIDER_DEFAULT
from win32security import error as LogonError
    
# Global class references -- these will be set when the Provider is initialised.
smb_domain = None

class SoSmbIdentityProvider(SqlObjectIdentityProvider):
    '''
    IdentityProvider that uses a model from a database (via SQLObject).
    '''
    
    def __init__(self):
        super(SoSmbIdentityProvider, self).__init__()
        get = turbogears.config.get
        global smb_domain
        smb_domain = get("identity.sosmbprovider.smb_domain", None)
            
    def validate_password(self, user, user_name, password):
        '''
        Validates user_name and password against a Windows/Samba domain
        specified in the identity.sosmbprovider.smb_domain config parameter.
        It's just a wrapper for win32security.LogonUser().
        '''
        global smb_domain
        try:
            token = LogonUser(user_name, 
                              smb_domain, 
                              password, 
                              LOGON32_LOGON_NETWORK,
                              LOGON32_PROVIDER_DEFAULT)
        except LogonError, e:
            return False
        else:
            return bool(token)   # usually True
