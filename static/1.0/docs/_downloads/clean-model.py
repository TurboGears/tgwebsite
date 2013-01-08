"""
this is the data model for the project
"""
__revision__ = "$Revision"

from datetime import datetime

from turbogears.database import PackageHub
import sqlobject as orm
from turbogears import identity 

HUB = PackageHub("sonar")
__connection__ = HUB

# class YourDataClass(SQLObject):
#     pass

# identity models.
class Visit(orm.SQLObject): #pylint: disable-msg=R0904
    """
    keep track of user visits
    """
    class sqlmeta:  #pylint: disable-msg=C0103,R0903
        """
        names like "Group", "Order" and "User" are reserved words in SQL
        so we set the name to something safe for SQL
        """
        table = "visit"

    visit_key = orm.col.StringCol(length=40, alternateID=True,
                          alternateMethodName="by_visit_key")
    created = orm.col.DateTimeCol(default=datetime.now)
    expiry = orm.col.DateTimeCol()

    def lookup_visit(cls, visit_key):
        """
        create an alternate lookup method using the  visit_key
        """
        try:
            return cls.by_visit_key(visit_key)  #pylint: disable-msg=E1101
        except orm.SQLObjectNotFound:
            return None
    lookup_visit = classmethod(lookup_visit)

class VisitIdentity(orm.SQLObject): #pylint: disable-msg=R0904
    """
    used to connect visits to a user
    """
    visit_key = orm.col.StringCol(length=40, alternateID=True,
                          alternateMethodName="by_visit_key")
    user_id = orm.col.IntCol()


class Group(orm.SQLObject): #pylint: disable-msg=R0904
    """
    An ultra-simple group definition.
    """
    class sqlmeta:  #pylint: disable-msg=C0103,R0903
        """
        names like "Group", "Order" and "User" are reserved words in SQL
        so we set the name to something safe for SQL
        """
        table = "tg_group"

    group_name = orm.col.UnicodeCol(length=16, alternateID=True,
                            alternateMethodName="by_group_name")
    display_name = orm.col.UnicodeCol(length=255)
    created = orm.col.DateTimeCol(default=datetime.now)

    # collection of all users belonging to this group
    users = orm.RelatedJoin("User", intermediateTable="user_group",
                        joinColumn="group_id", otherColumn="user_id")

    # collection of all permissions for this group
    permissions = orm.RelatedJoin("Permission", joinColumn="group_id", 
                              intermediateTable="group_permission",
                              otherColumn="permission_id")


class User(orm.SQLObject):  #pylint: disable-msg=R0904
    """
    Reasonably basic User definition. Probably would want additional attributes.
    """
    class sqlmeta:  #pylint: disable-msg=C0103,R0903
        """
        names like "Group", "Order" and "User" are reserved words in SQL
        so we set the name to something safe for SQL
        """
        table = "tg_user"

    user_name = orm.col.UnicodeCol(length=16, alternateID=True,
                           alternateMethodName="by_user_name")
    email_address = orm.col.UnicodeCol(length=255, alternateID=True,
                               alternateMethodName="by_email_address")
    display_name = orm.col.UnicodeCol(length=255)
    password = orm.col.UnicodeCol(length=40)
    created = orm.col.DateTimeCol(default=datetime.now)

    # groups this user belongs to
    groups = orm.RelatedJoin("Group", intermediateTable="user_group",
                         joinColumn="user_id", otherColumn="group_id")

    def _get_permissions(self):
        """
        return the permissions
        """
        perms = set()
        for group in self.groups:
            perms = perms | set(group.permissions)
        return perms

    def _set_password(self, cleartext_password):
        "Runs cleartext_password through the hash algorithm before saving."
        password_hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(password_hash)    #pylint: disable-msg=E1101

    def set_password_raw(self, password):
        "Saves the password as-is to the database."
        self._SO_set_password(password) #pylint: disable-msg=E1101



class Permission(orm.SQLObject):    #pylint: disable-msg=R0904
    """
    basic permission model
    """
    permission_name = orm.col.UnicodeCol(length=16, alternateID=True,
                                 alternateMethodName="by_permission_name")
    description = orm.col.UnicodeCol(length=255)

    groups = orm.RelatedJoin("Group",
                        intermediateTable="group_permission",
                         joinColumn="permission_id", 
                         otherColumn="group_id")
