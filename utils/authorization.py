class AuthorizationEnums:
    MANAGE_USERS = "manage_users"
    MANAGE_ORGANIZATIONS = "manage_organizations"
    MANAGE_FLOORS = "manage_floors"
    MANAGE_ROOMS = "manage_rooms"
    MANAGE_BOOKINGS = "manage_bookings"


class Authorization:

    @classmethod
    def get_admin_permissions(cls):
        """Returns all the permissions to be assigned to admin user"""
        return {
            AuthorizationEnums.MANAGE_USERS: 1,
            AuthorizationEnums.MANAGE_ORGANIZATIONS: 1,
            AuthorizationEnums.MANAGE_FLOORS: 1,
            AuthorizationEnums.MANAGE_ROOMS: 1,
            # AuthorizationEnums.MANAGE_BOOKINGS: 1
        }

    @classmethod
    def get_user_permissions(cls):
        """Returns all the permissions to be assigned to organization user"""
        return {
            AuthorizationEnums.MANAGE_BOOKINGS: 1
        }

    @classmethod
    def can_manage_users(cls, requestor_details):
        """Checks whether a user can perform operations on users table"""
        if not requestor_details:
            return False
        permissions = requestor_details.get("permissions", {})
        if AuthorizationEnums.MANAGE_USERS in permissions:
            return True
        return False

    @classmethod
    def can_manage_organizations(cls, requestor_details):
        """Checks whether a user can perform operations on organizations table"""
        if not requestor_details:
            return False
        permissions = requestor_details.get("permissions", {})
        if AuthorizationEnums.MANAGE_ORGANIZATIONS in permissions:
            return True
        return False

    @classmethod
    def can_manage_floors(cls, requestor_details):
        """Checks whether a user can perform operations on floors table"""
        if not requestor_details:
            return False
        permissions = requestor_details.get("permissions", {})
        if AuthorizationEnums.MANAGE_FLOORS in permissions:
            return True
        return False

    @classmethod
    def can_manage_rooms(cls, requestor_details):
        """Checks whether a user can perform operations on rooms table"""
        if not requestor_details:
            return False
        permissions = requestor_details.get("permissions", {})
        if AuthorizationEnums.MANAGE_ROOMS in permissions:
            return True
        return False

    @classmethod
    def can_manage_bookings(cls, requestor_details):
        """Checks whether a user can perform operations on Bookings table"""
        if not requestor_details:
            return False
        permissions = requestor_details.get("permissions", {})
        if AuthorizationEnums.MANAGE_BOOKINGS in permissions:
            return True
        return False
